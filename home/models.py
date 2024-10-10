from django.db import models
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from wagtail.fields import RichTextField

from wagtail.models import Page

from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField

# import MultiFieldPanel:
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class HomePage(Page):

    hero_text = RichTextField(
        blank=True,
        max_length=255, help_text="Write an introduction for the site"
    )

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