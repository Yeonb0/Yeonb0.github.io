---
title: "Ruby"
layout: archive
permalink: categories/ruby
author_profile: true
sidebar_main: true
---

{% assign posts = site.categories.Ruby %}
{% for post in posts %} {% include archive-single.html type=page.entries_layout %} {% endfor %}
