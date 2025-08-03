# 📄 Data Card: YouTube Video Metrics Dataset (YouTube Data API v3)

## 🧾 Dataset Summary

This dataset is collected using the YouTube Data API v3 and contains metadata and performance metrics for a set of public YouTube videos across various categories and countries. It includes publishing data, channel information, and engagement metrics at two points in time (initial and final logging). Here in this data collection, 1 hour time gap is considered for initial and final logging. It is suitable for video performance analysis, viewership prediction, and content recommendation systems.

---

## 📚 Dataset Details

| Feature Name                  | Description                                           | Type        |
| ----------------------------- | ----------------------------------------------------- | ----------- |
| video\_id                     | Unique identifier of the video                        | Text        |
| published\_at                 | Date and time when the video was published            | Timestamp   |
| title                         | Title of the video                                    | Text        |
| description                   | Description text of the video                         | Text        |
| category\_id                  | ID representing the content category                  | Numerical   |
| country                       | Country where the video/channel is primarily targeted | Categorical |
| tags                          | Tags assigned to the video                            | List/Text   |
| definition                    | Video quality definition (e.g., hd, sd)               | Categorical |
| channel\_id                   | Unique ID of the video’s channel                      | Text        |
| channel\_title                | Title of the YouTube channel                          | Text        |
| logged\_at\_initial           | Initial logging timestamp                             | Timestamp   |
| view\_count\_initial          | Initial view count at first logging                   | Numerical   |
| like\_count\_initial          | Initial like count at first logging                   | Numerical   |
| comment\_count\_initial       | Initial comment count at first logging                | Numerical   |
| c\_view\_count\_initial       | Initial total channel view count                      | Numerical   |
| c\_subscriber\_count\_initial | Initial channel subscriber count                      | Numerical   |
| logged\_at\_final             | Final logging timestamp (1 hour from initial logging) | Timestamp   |
| view\_count\_final            | Final view count after observation period             | Numerical   |
| like\_count\_final            | Final like count                                      | Numerical   |
| comment\_count\_final         | Final comment count                                   | Numerical   |
| c\_view\_count\_final         | Final channel view count                              | Numerical   |
| c\_subscriber\_count\_final   | Final channel subscriber count                        | Numerical   |

---

## 🏁 Motivation

The dataset was created to study YouTube video performance dynamics over time. It helps answer questions such as:

* How quickly do videos gain views, likes, or comments?
* Are some categories or countries associated with better video performance?
* What is the relationship between a channel's popularity and a video's early traction?

---

## 🛠️ Data Collection Process

* The dataset is collected automatically using a Python-based tool that interfaces with the YouTube Data API v3.
* A cron job is configured to execute the scraping script every hour throughout the day.
* During each hourly run (e.g., at 08:00), the script fetches all publicly available videos published in the previous hour (i.e., from 07:00 to 08:00).
* Immediately after discovery, an initial logging is performed, capturing:
* Video metadata (e.g., title, tags, category, country)
* Video-level performance metrics (e.g., views, likes, comments)
* Channel-level metadata (e.g., channel title, total views, subscribers)
* One hour later (e.g., at 09:00), a final logging is conducted for the same set of video IDs to observe engagement changes over the 1-hour interval.
* The process allows tracking of short-term performance evolution, helpful for early trend prediction and video growth modeling.
* Video categories are mapped using the standard videoCategoryId definitions provided by YouTube.
* Only public videos from a curated list of targeted countries and categories are included in the dataset.
---

## 🧼 Preprocessing

* (to be filled)
---

## ✅ Intended Use

This dataset supports:

* Regression/classification models to predict video popularity
* Category-wise trend analysis
* Country-level content performance studies
* Educational and research purposes in media analytics

---

## ⚠️ Ethical Considerations

* All data comes from public YouTube metadata, no private user info is used.
* Country codes are based on the default region set in YouTube API.
* No re-distribution of video content or thumbnails.
* Use responsibly, respecting YouTube's [Terms of Service](https://www.youtube.com/t/terms).

---

## 📜 License

This dataset is made available under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.

---

## 🧾 Citation

If you use this dataset, please cite:

```
@dataset{youtube_metrics_2025,
  title={YouTube Video Metrics Dataset},
  author={Parishith, Birunthaban, Aadithyan},
  year={2025},
  url={https://github.com/ragupari/youtube-data-scrapper}
}
```