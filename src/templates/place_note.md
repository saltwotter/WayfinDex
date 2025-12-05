# {{name}}

## Overview

**Category:** {{category}}  
**Address:** {{address}}  
{% if website %}**Website:** {{website}}{% endif %}

## Description

{{description}}

## Hours

{{open_hours}}

## Tips

{% for tip in tips %}

- {{tip}}
  {% endfor %}
