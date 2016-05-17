# ECCU Publisher

This project provides a command-line tool for publishing "ECCU" files to Akamai. ECCU is one of several mechanisms for programattically interacting with your Akamai cache. Unfortunately, there appears to be no public-facing dcoumentation of the format. You can publish one or several ECCU files at once, or pass in a list of URL paths that will be converted into the appropriate XML. This project is distributed as a Python package.

Current status: 1.0. This appears to solve the problems it, but we will almost certainly learn new things as we move towards actually implementing this.


## Dependencies

This software has only been tested under Python 2.6 and 2.7, on Mac OS X and Linux. It depends on the following Python libraries:

- [Suds](https://fedorahosted.org/suds/)
- [lxml](http://lxml.de/)
- [argparse](http://code.google.com/p/argparse/) (if running under Python 2.6)

## Installation
Into your Django Project:
```pip install git+https://github.com/cfpb/publish_eccu.git#egg=publish_eccu```

- Include `publish_eccu` as an INSTALLED_APPS

With PIP:

```pip install [path to downloaded zip file or checkout directory]```

Otherwise:

```bash
cd [path to checkout directory]
python setup.py install
```

## Usage

There are four important environment variables that must be set.

```bash
export AKAMAI_USER=[akamai account name]
export AKAMAI_PASSWORD=[akamai_password]
export AKAMAI_NOTIFY_EMAIL=[email to recieve success or failure notification]
export AKAMAI_HOST=[domain name you are acting on]
```

Then, to publish already-crafted ECCU XML files, invoke the tool like this:

```bash
publish_eccu foo.xml bar.xml
```

This will combine those files into a single ECCU, before posting.

For the simplest cases, you can pass URL paths instead of XML files:

```bash
publish_eccu --simple /about-us/contact /blog/
```

If you want to invalidate the root URL of the domain, pass along the --home argument:


```bash
publish_eccu --simple /about-us/contact /blog/ --home
```

Finally, if you just want to *see* the combined or generated XML, pass the --noop argument:

```bash
publish_eccu --simple /about-us/contact /blog/ --home --noop
successfully published:
---------
<eccu><match:recursive-dirs  value="about-us"><match:recursive-dirs value="contact"><revalidate>now</revalidate></match:recursive-dirs></match:recursive-dirs><match:recursive-dirs  value="blog"><revalidate>now</revalidate></match:recursive-dirs><match:this-dir  value="This Directory Only"><match:filename value="No File Specified"><revalidate>now</revalidate></match:filename></match:this-dir></eccu>
```
## How to test the software

Install dependencies
- `pip install -r requirements/test.txt`
- from the root directory of the project, run the `nosetests` command.

## Known issues

We'll surely discover some soon!

## Getting help


If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker.

## Getting involved

If you find this tool useful, (or *almost* useful, pending some particular improvements), get in touch!
General instructions on _how_ to contribute should be stated with a link to [CONTRIBUTING](CONTRIBUTING.md).


----

## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)


----

## Credits and references

1. Projects that inspired you
2. Related projects
3. Books, papers, talks, or other sources that have meaniginful impact or influence on this project 
