---
title: "How To Use Tool Calling To Build a Football Agent"
subtitle: "A basic stats analyst use case"
date: "2026-05-26"
url: "https://ricardoheredia.substack.com/p/how-to-use-tool-calling-to-build"
slug: "how-to-use-tool-calling-to-build"
wordcount_substack: 1053
reactions: 2
restacks: 1
comments: 0
---

You may have seen people trying to build agents using different solutions, with code, no-code/low-code alternatives, different frameworks and models, depending on the use case.

There’s not just one way of building them, it depends on what you want to achieve and the level of control you want to have over your agentic system.

Today, I want to talk to you about a real use case applied to football so you can see how is it to define the scope of building an agent, the rationale behind choosing certain tools, the errors, and thoughts on the process.

### A Basic Stats Analyst

I recently built an agent with my teammates during the [Context Engineering course by Twelve Football](https://twelve.football/courses/context-engineering-for-football) that finished just a couple weeks ago.

[![](https://substackcdn.com/image/fetch/$s_!8iyP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc5b80ab-c5ba-44ca-99e7-6af2a36d8085_2220x1286.heic)](https://substackcdn.com/image/fetch/$s_!8iyP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc5b80ab-c5ba-44ca-99e7-6af2a36d8085_2220x1286.heic) Screenshot of the Streamlit demo

The goal was to build a basic stats analyst agent that answered questions grounded on the Premier League 2024/2025 season dataset from Wyscout.

For that we used a defined set of tools:

- Pydantic models for data validation and structured outputs

- OpenAI tool calling

- DuckDB as our light weight SQL and vector database

- OpenAI LLM and embeddings models

- Streamlit as frontend for demo purposes

Down the road, we found out these were our preferred tools to build it, but it started out slightly different.

### The First Version (v1)

In the beginning we had a shaky Python script with ~1,400 lines of regex code that relied heavily on pattern matching, and it broke every time we asked something different.

The LLM was giving responses but only those that were included in the if/else loops.

[![](https://substackcdn.com/image/fetch/$s_!VZjb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F16114b65-adb7-4505-98fa-f8fc84d3f5c4_1764x554.heic)](https://substackcdn.com/image/fetch/$s_!VZjb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F16114b65-adb7-4505-98fa-f8fc84d3f5c4_1764x554.heic)

Questions like these were answered pretty well, but if you wanted to follow up the conversation, it lost context entirely. Also note that the wording is too verbose on metrics, a weird way to display the stats cause nobody talks like that.

So with every new question, we needed to patch more code.

We weren’t using the LLM properly to interrogate the dataset well.

### The Data Goes First

Before any answer reached the user, it had to pass through two data layers.

The first was **Pydantic**. We used it both to structured the output and to evaluate the responses against our questions benchmark. The LLM returned a verdict whether an answer was faithful or correct against a typed schema that matched our benchmark.

`passed: bool`, `reason: str`.

If the output didn’t match, it failed explicitly to avoid wrong responses and data leakage downstream.

The second was **[DuckDB](https://duckdb.org/)**, a lightweight SQL database that runs in-process without servers or heavy infrastructure. It read the Wyscout parquet files natively and, through its vector similarity extension (VSS), also stored the player and team embeddings for name resolution. Giving us the power of SQL queries and vector storage in the same tables.

Both of these were used to making sure the data the agent worked with was grounded data and it gave back grounded answers.

[![](https://substackcdn.com/image/fetch/$s_!sb1R!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F38f042ce-bb30-488f-b22c-8e92f33d25e2_1280x1142.heic)](https://substackcdn.com/image/fetch/$s_!sb1R!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F38f042ce-bb30-488f-b22c-8e92f33d25e2_1280x1142.heic) DuckD Database Schema.

### How the Tools Work (v2)

Now with the data layer in place, we needed the agent to actually use it.

So we used **Tool calling**.

It is how the LLM interacts with the database without touching it directly. The user asks a question, the LLM decides which tool to call and with what parameters, Python executes it against DuckDB, the result comes back, and the LLM writes the answer from that data.

We defined 4 tools: `query_player_stats`, `query_team_stats`, `query_ranking`, and `get_league_standings`.

Each tool has a name, a description, and a parameters schema. The description is what the LLM reads to decide whether to use it. The parameters tell it what arguments to pass.

Here’s how we defined the position filter inside `query_player_stats`:

[![](https://substackcdn.com/image/fetch/$s_!7fnl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94217e84-a434-46b6-ac4e-f435b4abf14a_1090x906.heic)](https://substackcdn.com/image/fetch/$s_!7fnl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94217e84-a434-46b6-ac4e-f435b4abf14a_1090x906.heic)

That description is doing what you’d write as a Python dictionary. The alias mapping, the edge cases, and the `forward` exception all lives in a string the LLM reads at inference time.

And it worked.

Here’s the agent handling a multi-step question about Salah, where it had to build a custom opponent bucket, compare it against the rest of the season, then filter again by Champions League teams, all in the same conversation:

[![](https://substackcdn.com/image/fetch/$s_!k2cP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9a6f1a3-c49c-405a-9d5d-72a67f8a4652_706x595.heic)](https://substackcdn.com/image/fetch/$s_!k2cP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9a6f1a3-c49c-405a-9d5d-72a67f8a4652_706x595.heic) Questions answers about a player in many turns.

But we started with 9 tools.

There were separate tools for top scorers, best passers, most progressive carriers, each its own function.

The problem was the LLM kept picking the wrong one because the descriptions overlapped. It would call `get_top_scorers` when it should have called `query_ranking` with `metric=goals`.

So we merged them down to 4, with broader scope and cleaner descriptions.

Going from 9 to 4 reduced routing errors more than any prompt tweak we tried. With fewer tools the LLM had fewer decisions to get wrong.

While building the position filter, we had a Python dictionary in `agent_tools.py` that mapped user aliases to database values at execution time.

Every time the LLM passed `"CB"`, Python caught it and translated it to `"Central Defender"`.

It worked. But we deleted it.

[![](https://substackcdn.com/image/fetch/$s_!YvXb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F042f3740-0d2f-4958-85df-1c36b588ae59_930x532.heic)](https://substackcdn.com/image/fetch/$s_!YvXb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F042f3740-0d2f-4958-85df-1c36b588ae59_930x532.heic)

We realized the same logic could live in the tool description instead. If you write it clearly enough, like documentation, the LLM passes the right value before the code ever runs.

### **Memory**

In v1, the conversation had no memory between turns. If you followed up on a question, the context was entirely lost.

We fixed it with one line of code using the OpenAI Responses API. It kept the conversation state through `previous_response_id`. You pass the last response ID and the API handles the rest.

This how it looks in code:

[![](https://substackcdn.com/image/fetch/$s_!eqwt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb79a6aca-9941-41da-bb3c-24942181fe75_1040x720.heic)](https://substackcdn.com/image/fetch/$s_!eqwt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb79a6aca-9941-41da-bb3c-24942181fe75_1040x720.heic)

This is how it looked in the Streamlit UI:

[![](https://substackcdn.com/image/fetch/$s_!Khk0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2817517e-e62d-4aa3-82fa-c39244b92fa0_706x387.jpeg)](https://substackcdn.com/image/fetch/$s_!Khk0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2817517e-e62d-4aa3-82fa-c39244b92fa0_706x387.jpeg) Salah follow-up chain

### How We Knew It Worked

We built a benchmark of 61 questions and ran it after every change we made. Each answer was scored by an LLM judge against the expected output, so we didn't have to go through them manually.

At the end, we threw 21 random questions at it that none of us had prepared for. It got 21 out of 21.

[![](https://substackcdn.com/image/fetch/$s_!LtIY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ecbb18a-99c4-4d60-8199-ffd50e47f12a_726x249.jpeg)](https://substackcdn.com/image/fetch/$s_!LtIY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ecbb18a-99c4-4d60-8199-ffd50e47f12a_726x249.jpeg)

The screenshot also shows the agent refusing questions it can't answer. That's something we had to build explicitly in order to make it refuse out of scope questions and not hallucinated.

### Wrapping Up

Right now it only covers the Premier League 2024/25. Just one league and one season.

The interesting question is whether the same approach holds when you scale it. More leagues, more seasons, harder questions.

That’s what we want to find out next.

Till next time,

Ricardo.

[![Ricardo Heredia's avatar](https://substackcdn.com/image/fetch/$s_!ddIT!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d582183-8bb5-43cc-ab1a-620ca5f196c5_1200x1500.jpeg)](https://substack.com/profile/313134153-ricardo-heredia)[![Donato's avatar](https://substackcdn.com/image/fetch/$s_!j8MV!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F77a63984-c716-4a87-be69-741fe0ea11e8_1165x1167.jpeg)](https://substack.com/profile/81308007-donato)

2 Likes∙
