import datetime
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from dataclasses import dataclass

# Path to TEMPLATES folder (relative to where you run the script)
PATH_TO_TEMPLATES = Path('../generator/TEMPLATES/')
# Path to RESOURCES folder (relative to where you run the script)
PATH_TO_RESOURCES = Path('../generator/RESOURCES/')
# Path to output folder (relative to where you run the script)
PATH_TO_OUTPUT = Path('../docs/')
# Root URL
URL_ROOT = "https://civicdatacooperative.com/"

# Link to homepage
link_to_homepage = "/"  # TODO: always '/' in production
# File suffix
html_file_suffix = ".html"


@dataclass()
class Page(object):
    title: str
    keywords: str
    description: str
    content_file: str
    url: str
    language: str
    last_mod: datetime.datetime
    name: str

    def keys(self):
        """Get keys that allows conversion of this class to dictionary.
        Returns:
            List[str]: List of the keys to be passed to template.
        """
        return ['title', 'keywords', 'description', 'url', 'content_file',
                'language', 'name']

    def __getitem__(self, key):
        """Allows conversion of this class to dictionary.
        """
        return getattr(self, key)

    def generate_site(self):
        with open(PATH_TO_TEMPLATES.joinpath('page.html')) as tem_han:
            template = Environment(
                loader=FileSystemLoader(PATH_TO_TEMPLATES)
            ).from_string(tem_han.read())
            html_str = template.render(
                **dict(self),
                link_to_homepage=link_to_homepage
            )
            return html_str

    @property
    def absolute_url(self):
        if self.url != 'index':
            return URL_ROOT + self.url + html_file_suffix
        return URL_ROOT

    @property
    def last_modified(self):
        if self.last_mod is None:
            return None
        return self.last_mod.strftime('%Y-%m-%d')


# Common meta tags
comm_keywords: str = "CIPHA, civic, data, synthetic, CPRD"
comm_description: str = "The Civic Data Cooperative is a part of the Faculty of Health and Life Sciences at the University of Liverpool working on projects that operate with data about citizens."  # noqa: E501


# Pages definition
pages = [
    Page(title="Liverpool City Region Civic Data Cooperative",
         keywords=comm_keywords,  # noqa: E501
         description=comm_description,  # noqa: E501
         url="index",
         content_file='page_home.html',
         language="en",
         last_mod=datetime.datetime(2022, 1, 1),
         name="Home"
         ),
    Page(title="LCR Civic Data Cooperative: About us",
         keywords=comm_keywords,  # noqa: E501
         description=comm_description,  # noqa: E501
         url="about",
         content_file='page_about.html',
         language="en",
         last_mod=datetime.datetime(2022, 1, 1),
         name="About Us"
         ),
    Page(title="LCR Civic Data Cooperative: Mission",
         keywords=comm_keywords,  # noqa: E501
         description=comm_description,  # noqa: E501
         url="mission",
         content_file='page_mission.html',
         language="en",
         last_mod=datetime.datetime(2022, 1, 1),
         name="Mission"
         ),
    Page(title="LCR Civic Data Cooperative: Contact",
         keywords=comm_keywords,  # noqa: E501
         description=comm_description,  # noqa: E501
         url="contact",
         content_file='page_contact.html',
         language="en",
         last_mod=datetime.datetime(2022, 1, 1),
         name="Contact"
         ),
    Page(title="LCR Civic Data Cooperative: License",
         keywords=comm_keywords,  # noqa: E501
         description=comm_description,  # noqa: E501
         url="license",
         content_file='page_license.html',
         language="en",
         last_mod=datetime.datetime(2022, 1, 1),
         name="License"
         ),
]

# Remove all existing resources
if PATH_TO_OUTPUT.exists():
    shutil.rmtree(PATH_TO_OUTPUT)

# Create new dir
PATH_TO_OUTPUT.mkdir()

for page in pages:
    content = page.generate_site()
    with PATH_TO_OUTPUT.joinpath(page.url + html_file_suffix).open('w') as fp:
        fp.write(content)

# Copy resources
shutil.copytree(PATH_TO_RESOURCES, PATH_TO_OUTPUT, dirs_exist_ok=True)

# Generate site map (XML):
with open(PATH_TO_TEMPLATES.joinpath('site_map.xml')) as tem_han:
    template = Environment(
        loader=FileSystemLoader(PATH_TO_TEMPLATES)
    ).from_string(tem_han.read())
    html_str = template.render(
        sites=pages
    )
    with PATH_TO_OUTPUT.joinpath('sitemap.xml').open('w') as f_xml:
        f_xml.write(html_str)

# Generate robots.txt file
robots_txt_content = f"""User-agent: *
Allow: /
Sitemap: {URL_ROOT}sitemap.xml"""
with PATH_TO_OUTPUT.joinpath('robots.txt').open('w') as robots_txt_h:
    robots_txt_h.write(robots_txt_content)
