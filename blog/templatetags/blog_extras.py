# blog/templatetags/blog_extras.py

import re
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()

@register.filter
def highlight(text, search_term):
    """
    Highlights search terms in text with HTML markup.
    Usage: {{ text|highlight:search_term }}
    """
    if not search_term or not text:
        return text
    
    # Escape HTML in both text and search term to prevent XSS
    escaped_text = escape(str(text))
    escaped_search = escape(str(search_term))
    
    # Create a regex pattern for case-insensitive search
    pattern = re.compile(re.escape(escaped_search), re.IGNORECASE)
    
    # Replace matches with highlighted version
    highlighted = pattern.sub(
        f'<span class="search-highlight">{escaped_search}</span>',
        escaped_text
    )
    
    # Return as safe HTML
    return mark_safe(highlighted)

@register.filter
def truncate_highlight(text, args):
    """
    Truncates text and then highlights search terms.
    Usage: {{ text|truncate_highlight:"20,search_term" }}
    """
    try:
        words_count, search_term = args.split(',', 1)
        words_count = int(words_count)
    except (ValueError, AttributeError):
        return text
    
    # Truncate words first
    words = str(text).split()
    if len(words) > words_count:
        truncated = ' '.join(words[:words_count]) + '...'
    else:
        truncated = text
    
    # Then apply highlighting
    return highlight(truncated, search_term)

@register.filter
def smart_truncate(text, length=100):
    """
    Smart truncation that doesn't cut words in half.
    Usage: {{ text|smart_truncate:100 }}
    """
    if not text:
        return ""
    
    text = str(text)
    if len(text) <= length:
        return text
    
    # Find the last space before the length limit
    truncated = text[:length]
    last_space = truncated.rfind(' ')
    
    if last_space > 0:
        truncated = truncated[:last_space]
    
    return truncated + '...'

@register.simple_tag
def search_result_count(posts, search_term):
    """
    Returns formatted search result count.
    Usage: {% search_result_count posts request.GET.search %}
    """
    count = posts.paginator.count if hasattr(posts, 'paginator') else 0
    
    if search_term:
        return f'Found {count} result{"s" if count != 1 else ""} for "{search_term}"'
    else:
        return f'Showing {count} post{"s" if count != 1 else ""}'

@register.inclusion_tag('blog/snippets/pagination_info.html')
def pagination_info(page_obj):
    """
    Renders pagination information.
    Usage: {% pagination_info posts %}
    """
    return {
        'page_obj': page_obj,
        'start_index': page_obj.start_index() if hasattr(page_obj, 'start_index') else 1,
        'end_index': page_obj.end_index() if hasattr(page_obj, 'end_index') else page_obj.paginator.count,
        'total_count': page_obj.paginator.count,
    }

@register.filter
def add_class(field, css_class):
    """
    Adds CSS class to form field.
    Usage: {{ form.field|add_class:"form-control" }}
    """
    return field.as_widget(attrs={'class': css_class})

@register.filter
def multiply(value, multiplier):
    """
    Multiplies value by multiplier.
    Usage: {{ value|multiply:2 }}
    """
    try:
        return int(value) * int(multiplier)
    except (ValueError, TypeError):
        return 0