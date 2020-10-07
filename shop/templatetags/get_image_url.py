from django import template

register = template.Library()

@register.simple_tag(name='get_image_url')
def get_image_url(img):
  return img.url
