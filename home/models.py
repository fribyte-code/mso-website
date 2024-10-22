from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class DefaultPage(Page):

    # We use RichTextField for text fields
    # so that the client can format the text as they like.

    # Hero_text is the subtitle of the page
    hero_text = RichTextField(
        blank=True,
        max_length=255, help_text="Write an introduction for the site"
    )

    # This is the body of the text
    body = RichTextField(blank=True, help_text="Write a body for your site")

    # modify your content_panels:
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_text"),
            ],
            heading="Hero section",
        ),
        FieldPanel('body'),
    ]

def get_nav_pages(self):
    return self.get_children().live().public()