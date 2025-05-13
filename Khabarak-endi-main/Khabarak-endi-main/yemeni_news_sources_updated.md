# Yemeni News Sources

This document lists reliable Yemeni news sources that will be used for our news aggregator website "خبرك عندي". These sources have been identified based on their presence on sahafah.net and their focus on Yemeni news.

## Primary News Sources

1. **24 بوست (24 Post)**
   - Focus: General Yemeni news
   - URL: https://www.24-post.com/
   - Status: Active
   - Categories: Politics, Local news

2. **أبابيل نت (Ababeel Net)**
   - Focus: Yemeni news
   - URL: https://yemeninews.net/source22.html
   - Status: Active
   - Categories: General news

3. **أحداث نت (Ahdath Net)**
   - Focus: Yemeni news
   - URL: Domain parked (ahdathnet.net)
   - Status: Inactive/Unavailable
   - Categories: General news

4. **أنباء عدن (Anbaa Aden)**
   - Focus: News from Aden region
   - URL: https://www.anbaaden.com/ (based on observed navigation)
   - Status: Active
   - Categories: Local news, Politics

5. **كريتر سكاي (Crater Sky)**
   - Focus: Local Yemeni news
   - URL: https://crater-sky.net/
   - Categories: Local news

6. **نيوز لاين (News Line)**
   - Focus: Yemeni news
   - URL: https://newsline-ye.com/
   - Categories: Yemen news

7. **اليمني الجديد (The New Yemeni)**
   - Focus: Yemeni news
   - URL: https://www.alyemenialjadid.net/
   - Categories: Local news

8. **الإصلاح نت (Al-Islah Net)**
   - Focus: Political news
   - URL: https://alislah-ye.net/
   - Categories: Politics, Opinion

9. **الحرف 28 (Al-Harf 28)**
   - Focus: Yemeni cultural and opinion content
   - URL: https://alharf28.com/
   - Categories: Culture, Opinion

10. **الأول (Al-Awal)**
    - Focus: Yemeni news
    - URL: https://ym-now.net/
    - Categories: General news

## News Categories to Include

1. **أخبار محلية (Local News)**
   - News specific to different regions in Yemen

2. **أخبار اليمن (Yemen News)**
   - General news about Yemen

3. **سياسة (Politics)**
   - Political developments in Yemen

4. **اقتصاد (Economy)**
   - Economic news and analysis

5. **رياضة (Sports)**
   - Sports news from Yemen

6. **ثقافة (Culture)**
   - Cultural news and events

7. **مقالات (Articles/Opinion)**
   - Opinion pieces and analysis

8. **تقارير (Reports)**
   - In-depth reporting on Yemeni issues

## Content Aggregation Strategy

For each news source, we will need to:

1. Determine the best method for content aggregation:
   - RSS feeds (if available)
   - API access (if provided)
   - Web scraping (as a last resort, with proper attribution)

2. Set up regular content fetching intervals (e.g., hourly updates)

3. Implement content filtering to ensure only Yemen-related news is included

4. Ensure proper attribution to original sources

5. Categorize content based on the predefined categories

6. Store content in a database for efficient retrieval and display

## Findings from Source Analysis

Based on our initial research:
- Some Yemeni news websites are active and accessible (like 24 Post and Anbaa Aden)
- Some domains appear to be inactive or parked (like Ababeel Net and Ahdath Net)
- We will need to implement web scraping for most sources as they likely don't provide APIs
- All sources will require proper attribution with links back to the original articles
- We should implement a monitoring system to detect when sources change their structure or become unavailable

## Next Steps

- Complete research on remaining source URLs
- Develop scraping methods for active sources
- Create a database schema to store news articles with proper categorization
- Implement the content aggregation system
