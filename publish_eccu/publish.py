import argparse 
import base64
import os
import os.path
import codecs
import itertools

from lxml import etree
from suds.client import Client

parser = argparse.ArgumentParser(prog='publish_eccu',
                                 description="publish ECCU XML files to Akamai")

parser.add_argument('paths', nargs="+", help="One or more file names containing ECCU XML (if not using --simple as below)")
parser.add_argument('--simple', help="Treat arguments as URL paths", action='store_true')
parser.add_argument('--noop', help="Just output the genrated XML, without publishing", action='store_true')
parser.add_argument('--home', help="In addition to the other arguments, invalidate the page at /", action='store_true')

# I made this up....
MATCH_NAMESPACE = "http://akamai.com/eccuapi/match"
etree.register_namespace('match',MATCH_NAMESPACE)

def match_tag(name):
    """ etree uses tags in the form {namespace uri}tag"""
    return "{%s}%s" % (MATCH_NAMESPACE, name)


def invalidate_homepage_rule():
    """
    generate the pile of Elements that ECCU uses to say
    "invalidate the home page, please"
    """
    match_this_dir = etree.Element(match_tag("this-dir"), value="This Directory Only")
    match_filename = etree.Element(match_tag("filename"), value="No File Specified")
    revalidate = etree.Element('revalidate')
    revalidate.text = 'now'
    match_filename.append(revalidate)
    match_this_dir.append(match_filename)

    return [match_this_dir]

def scrub_namespaces(xml):
    """
    While etree freaks out about the lack of namespaces,
    ECCU freaks out WITH them.
    """
    no_namespaces = xml.replace('xmlns:match="%s"' % MATCH_NAMESPACE,"")
    return no_namespaces

def dirname_to_elements(dirname):
    """
    Convert a URL path of arbitrary depth, into nested recursice-dirs
    tags
    """
    current_tag = None
    for component in dirname.split('/'):
        if component:
            new_element = etree.Element("{%s}recursive-dirs" % MATCH_NAMESPACE, value=component)
            if current_tag is not None: 
                current_tag.append(new_element)
            else:
                root_tag = new_element

            current_tag = new_element

    revalidate_tag = etree.Element('revalidate')
    revalidate_tag.text='now'

    current_tag.append(revalidate_tag)
    return [root_tag]

def build_eccu_file(lists_of_rules):
    """
    Wrap the provided lists of Elements into a proper <eccu>
    document
    """
    eccu_root= etree.Element('eccu' )
    for rule in itertools.chain(*lists_of_rules):
        eccu_root.append(rule)

    combined_tree = etree.ElementTree(eccu_root)
    combined_document = etree.tostring(combined_tree)

    # the ECCU API rejects files that include a namespace delcaration for 'match'
    no_namespaces = combined_document.replace('xmlns:match="http://akamai.com/eccuapi/match"',"")
    return no_namespaces

def merge_eccu_files(paths):
    """
    Converts a list of paths (pointint to eccu XML files) to a lists of lists (one per file)
    each containing Elements extracted from the XML file
    """
    parsed_eccu_files = []

    # parse all of the XML files
    for path in paths:
        eccu_file = codecs.open(path,encoding='utf8')
        markup = eccu_file.read()
        markup = markup.replace('<eccu>', "<eccu xmlns:match='%s'>" % MATCH_NAMESPACE)
        tree = etree.fromstring(markup)
        parsed_eccu_files.append(tree)

    return [parsed.getchildren() for parsed in parsed_eccu_files]

def main():
    # Get credentials
    assert 'AKAMAI_USER' in os.environ, "AKAMAI_USER must be set" 
    assert 'AKAMAI_PASSWORD' in os.environ, "AKAMAI_PASSWORD must be set" 
    assert 'AKAMAI_HOST' in os.environ, "AKAMAI_HOST must be set"
    assert 'AKAMAI_NOTIFY' in os.environ, "AKAMAI_NOTIFY must be set"

    username = os.environ['AKAMAI_USER']
    password = os.environ['AKAMAI_PASSWORD']
    host = os.environ['AKAMAI_HOST']
    notify = os.environ['AKAMAI_NOTIFY']

    # Get path to WSDL file
    package_path = os.path.dirname(__file__)
    wsdl_path = os.path.join(package_path,'PublishECCU.xml')

    # build client
    client = Client('file://' + wsdl_path ,username=username, password= password)

    args = parser.parse_args()
    if args.simple:
        # treat args.paths as URL segments
        rules = [dirname_to_elements(url) for url in args.paths]
    else:
        # treat args.paths as XML paths
        rules = merge_eccu_files(args.paths)

    if args.home:
        rules.append(invalidate_homepage_rule())

    combined_eccu = build_eccu_file(rules)

    purgedata = base64.b64encode(combined_eccu)
    if not args.noop:
        client.service.upload('purge.data', purgedata, "uploaded by pusher",None, host,'hostheader', True, notify)
    print "successfully published:"
    print "---------"
    print combined_eccu

if __name__ == '__main__':
    main()

