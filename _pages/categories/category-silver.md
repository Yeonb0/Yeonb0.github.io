---
title: "Silver"
layout: archive
permalink: categories/silver
author_profile: true
sidebar_main: true
---

{% assign posts = site.categories.Silver %}
{% for post in posts %} {% include archive-single.html type=page.entries_layout %} {% endfor %}
