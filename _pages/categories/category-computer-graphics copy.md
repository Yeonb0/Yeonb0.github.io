---
title: "Computer Graphics"
layout: archive
permalink: /categories/computer-graphics/
author_profile: true
sidebar_main: true
---

{% assign posts = site.categories["Computer-Graphics"] %}
{% for post in posts %} {% include archive-single.html type=page.entries_layout %} {% endfor %}
