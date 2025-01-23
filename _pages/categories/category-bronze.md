---
title: "Bronze"
layout: archive
permalink: categories/bronze
author_profile: true
sidebar_main: true
---

{% assign posts = site.categories.Bronze %}
{% for post in posts %} {% include archive-single.html type=page.entries_layout %} {% endfor %}
