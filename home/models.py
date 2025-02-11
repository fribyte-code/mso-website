from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class HjemPage(Page):

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


class BestillingPage(Page):
    hero_text = RichTextField(
        blank=True,
        max_length=255, help_text="Write a title for the paragraph explaining how to order"
    )

    main_paragraph = RichTextField(blank=True, help_text="Write a paragraph explaining how to order")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_text"),
            ],
            heading="Hero section",
        ),
        FieldPanel('main_paragraph'),
    ]

class StyretPage(Page):
    main_paragraph = RichTextField(blank=True, help_text="Write a list over current members in the board")

    content_panels = Page.content_panels + [
        FieldPanel('main_paragraph'),
    ]

class SporossPage(Page):
    main_paragraph = RichTextField(blank=True, help_text="Info til de som skal utfylle spørreskjemaet")

    content_panels = Page.content_panels + [
        FieldPanel('main_paragraph'),
    ]

class AksjonsukePage(Page):
    main_paragraph = RichTextField(blank=True, help_text="Skriv den infoen du vil om aksjonsuken")

    content_panels = Page.content_panels + [
        FieldPanel('main_paragraph'),
    ]

class EvalueringPage(Page):
    main_paragraph = RichTextField(blank=True, help_text="Skriv den infoen du vil om evalueringen")

    content_panels = Page.content_panels + [
        FieldPanel('main_paragraph'),
    ]

