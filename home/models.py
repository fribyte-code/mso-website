from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

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

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

