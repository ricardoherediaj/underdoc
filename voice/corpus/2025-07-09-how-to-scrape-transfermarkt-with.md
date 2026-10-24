---
title: "How to Scrape Transfermarkt with Python: Data-Driven Player Recruitment using England’s Championship, League Two, and League One data."
subtitle: ""
date: "2025-07-09"
url: "https://ricardoheredia.substack.com/p/how-to-scrape-transfermarkt-with"
slug: "how-to-scrape-transfermarkt-with"
wordcount_substack: 1082
reactions: 28
restacks: 2
comments: 0
---

Web scraping has always intrigued me. In my opinion, is one of the best skills you can have in your data science/ML toolbox. It is useful for when you want to build your own custom databases for personal projects and you don’t have access to paid data providers.

# **Using Web Scraping For A Project**

I’ll show you how I approached a past project using web scraping. I wanted to identify two players profiles:

- A central midfielder with a mixed profile (good in both defense and attack)

- A striker with good aerial game and ball retention.

I focused on finding five players for each position that fit the profiles based on different metrics from FBRef, the team’s playing style and the economic context of the team, where Transfermarkt helps a lot with players value market.

For this, I randomly chose Sheffield United from the Championship to carry on with the analysis.

To get to know Sheffield’s playing style and what they needed I analyzed three matches and identified positions that could benefit from these signings.

> _For more insights on how to analyze a team performance you can read this post about how I applied this framework for Como 1907 from Serie A: [Como 1907 Team Analysis for Data Scouting](https://ricardoheredia.substack.com/p/the-art-of-football-data-scouting?r=56fjux)_

[![](https://substackcdn.com/image/fetch/$s_!reIY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7170ebc3-987f-4bb5-9272-b5c147adce2b_800x800.heic)](https://substackcdn.com/image/fetch/$s_!reIY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7170ebc3-987f-4bb5-9272-b5c147adce2b_800x800.heic)

### How to Know Players Value Market?

To achieve this, I needed to gather data from Transfermarkt.

For those unfamiliar with this web page, it is a place that offers a variety of data points that are helpful to identify potential players:

- Age.

- Country.

- Contract

- Positions

- Market values.

To do this efficiently, I needed an automated way to extract player information directly from Transfermarkt, which led me to build a web scraper.

# **Designing the Scraper: Building Process and Core Components**

In order to build the scraper, I first needed to understand what and how I was going to do it. So I wanted to see if somebody else did it first and fortunately, someone did. These two Medium articles were my go-to references to help me go through this task:

> _[https://blog.devgenius.io/get-to-know-the-greatest-football-league-in-the-world-with-python-and-transfermarkt-25a7cfa6b136](https://blog.devgenius.io/get-to-know-the-greatest-football-league-in-the-world-with-python-and-transfermarkt-25a7cfa6b136)_
>
> _[https://medium.com/@conalhenderson/how-to-build-a-custom-web-scraper-to-extract-premier-league-player-market-data-3b8e5378cca2](https://medium.com/@conalhenderson/how-to-build-a-custom-web-scraper-to-extract-premier-league-player-market-data-3b8e5378cca2)_

I specially followed Conal’s comprehensive tutorial to build my own custom web scraper, as he shows how to do it exactly but with Liverpool’s and Premier League data, so it was a matter of going through it, running the code and understanding the process that happens under the hood when scraping Transfermarkt.

It was challenging, honestly. But after a few days I managed to replicate the exact same process for my goal: obtaining England’s tier 2, 3 and 4 data.

The bright side, is that I learned a new way of web scraping and improved capabilities on Python coding, which is necessary for when you want your code to be more readable and scalable as your project grows.

I won’t get into each detail of the code though, if you’re looking to do some web scraping, I highly recommend following the tutorial to better understand step by step where everything comes from and the final output, since it requires some attention if you don’t know German (all of Transfermarkt source code is in German).

I’ll focus on the core parts I included in my pipeline.

So, to make the scraper as modular and efficient as possible, and using Python flexible capabilities, I designed it with some key components:

1. **Abstract Parser Class**: I used an Abstract Base Class (`Parser`) as a template for all specific parsers which helped obtain different types of player data.

As you’ll see in the image I focused on getting these data points from all the players: names, ages, countries, market values, and positions (plus the team and the season), because these were the ones I could get, somehow, I couldn’t manage to obtain other datapoints from the HTML source (got to look into that), but I believe these were the most helpful for my goal.

[![](https://substackcdn.com/image/fetch/$s_!WMW5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67e58b89-2aad-4199-b6a4-53a2a3d6964e_2000x1623.png)](https://substackcdn.com/image/fetch/$s_!WMW5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67e58b89-2aad-4199-b6a4-53a2a3d6964e_2000x1623.png)

By breaking the parsing into smaller, independent classes, you can maintain a cleaner code and made modifications easier in the feature without affecting other components.

**2\. Dataclasses for Structured Data**: To organize my code and ensure type safety, I used Python’s `dataclass` to create a `Team` class. This helped me encapsulate relevant information such as the team ID and name, and it was an efficient way to pass data around the scraper.

**3\. The Scraper Class**: It takes a team, a list of parsers, and then extracts data from Transfermarkt. The structure of the URL allowed for programmatic generation by passing in the team ID and name, making the whole process automated and highly scalable.

[![](https://substackcdn.com/image/fetch/$s_!4pkl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57c61305-aaff-4a9e-be55-1939fcc188e8_2000x1579.png)](https://substackcdn.com/image/fetch/$s_!4pkl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57c61305-aaff-4a9e-be55-1939fcc188e8_2000x1579.png)

This part of the code shows the main `Scraper` class I mentioned, which fetches data for a given team and year, and allows you to scale the scraping across different teams by utilizing a uniform URL structure.

It uses BeautifulSoup to retrieve the HTML and **httpx** with custom headers to mimic a browser. Also, using ‘time.sleep(5)’ is critical to use to avoid overwhelming the server, getting kicked out and blocked in the future.

[![](https://substackcdn.com/image/fetch/$s_!W7FN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff64ac657-444a-4571-95dd-980b8815cad9_1656x832.png)](https://substackcdn.com/image/fetch/$s_!W7FN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff64ac657-444a-4571-95dd-980b8815cad9_1656x832.png)

# **The Result: Structured CSV file ready to use for scouting analysis**

The final dataset included the information I meant to scrape: player names, ages, countries, positions, and market values, which I saved into CSV files for further analysis.

Additionally, I uploaded the data to Supabase in different SQL tables for each league to make it easily accessible for querying and integration with other tools afterwards.

[![](https://substackcdn.com/image/fetch/$s_!AM2W!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F406d4a5e-8fa0-4b8c-8e2c-45f82278a95f_1427x635.png)](https://substackcdn.com/image/fetch/$s_!AM2W!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F406d4a5e-8fa0-4b8c-8e2c-45f82278a95f_1427x635.png)

This allows me to have a central structured storage and to query this data quickly, be it inside Supabase or using a connection to that database and clean the data with Pandas in another development environment.

# **Key Takeaways**

- Handling the intricacies and best practices of web scraping is tough, but necessary to execute repetitive processes effectively.

- Breaking the code into modular pieces using classes and parsers, makes it easier to extend the scraper and add new features as needed.

- Storing the scraped data in a database helps to maintain a centralized storage for further analyses.

Here’s the link to project in case you want to reference the code: [Data Driven Scouting Project](https://github.com/ricardoherediaj/data-driven-scouting-project)

* * *

I’d love to hear your thoughts or discuss any challenges you’ve faced when web scraping data.

[Leave a comment](https://ricardoheredia.substack.com/p/how-to-scrape-transfermarkt-with/comments)

* * *

Thanks for reading till the end! Subscribe for free to read more about how you can apply data, ML and AI to football or your own niche.

[![Md Adnan's avatar](https://substackcdn.com/image/fetch/$s_!Daq2!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad7b8ab2-f030-47a6-b305-9f1037f3eff7_96x96.jpeg)](https://substack.com/profile/281032238-md-adnan)[![Flávio Amaral Vilela's avatar](https://substackcdn.com/image/fetch/$s_!Jrme!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F020f0a8a-71ff-4f35-aff5-9590ff00643d_582x582.png)](https://substack.com/profile/118041731-flavio-amaral-vilela)[![Philby's avatar](https://substackcdn.com/image/fetch/$s_!77aC!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1711e6e0-a1e1-4ec6-9b37-f60040c99846_400x400.jpeg)](https://substack.com/profile/4330967-philby)[![Daniel's avatar](https://substackcdn.com/image/fetch/$s_!d89F!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e67020f-69e4-4e6b-925b-618cd2229622_1024x1024.png)](https://substack.com/profile/358340163-daniel)[![Neif's avatar](https://substackcdn.com/image/fetch/$s_!kDuJ!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F087d895d-010e-44d5-abc8-d32f04b94879_96x96.jpeg)](https://substack.com/profile/314514878-neif)

28 Likes∙
