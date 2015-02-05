import publish

try:
        import unittest2 as unittest
except ImportError:
        import unittest

class TestXMLGeneration(unittest.TestCase):
    def test_homepage_xml(self):
        this_dir = publish.invalidate_homepage_rule()[0]
        self.assertEquals('{http://akamai.com/eccuapi/match}this-dir',this_dir.tag)
        self.assertEquals('This Directory Only', this_dir.attrib['value'])

    def test_match_tag(self):
        tag_name = publish.match_tag('foo')
        self.assertEquals('{http://akamai.com/eccuapi/match}foo', tag_name)

    def test_scrub_namespaces(self):
        ns_uri = "http://akamai.com/eccuapi/match"
        doc = '<eccu xmlns:match="%s"/>' % ns_uri
        result = publish.scrub_namespaces(doc)
        self.assertNotIn(ns_uri,result)

    def test_dirname_to_elements(self):
        rules = publish.dirname_to_elements('ask/bob')[0]
        self.assertEqual('ask', rules.attrib['value'])
        inner_rule = rules.getchildren()[0]
        self.assertEqual('bob', inner_rule.attrib['value'])

    def test_build_eccu_file(self):
        rules = publish.dirname_to_elements('ask/bob')
        xml_doc = publish.build_eccu_file([rules])
        expected_doc='<eccu><match:recursive-dirs  value="ask"><match:recursive-dirs value="bob"><revalidate>now</revalidate></match:recursive-dirs></match:recursive-dirs></eccu>'
        self.assertEquals(xml_doc, expected_doc)
        import pdb;pdb.set_trace()
