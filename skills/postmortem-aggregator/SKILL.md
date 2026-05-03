---
name: postmortem-aggregator
description: 💀 [SRE] To be used when you have a folder containing N Post Mortem files. This will help crunch data and maintain/update a POMO_AGGREGATED.md file
metadata:
  version: 0.1.0
compatibility: Gemini CLI
---

# Identify the PoMos

* If the pomos are local in a folder, use those.
* If they're external, create a new folder called `YYYYMMDD_POSTMORTEMS/` and copy their MD version there. This might lose information, but ensure the relevant info is transported here, locally. You could run the "postmortem generator" skill on a locally curled page.
* If there is ONE, refuse to run this.
* If there is 2-3, suggest the user it's worth using a plurality of these.

## Action

Check all the Post Mortems in the folder and identify these informations:

1. Timestamp of outage start.
1. Timestamp of outage identified by human and being worked on (if available).
1. Timestamp of first Mitigation going into place (if available)
1. Timestamp of outage end.
1. Product used (eg Cloud, Youtube). Products could have a taxonomy (eg `Cloud::GCE::PersistentDisk`, `Youtube::Playlists`)
1. RootCause class (HUMAN_ERROR, CONFIG_CHANGE, EXTERNAL_CAUSE, ..).
1. Outage size, how bad it was (TEST, NEGLIGIBLE, SMALL, MEDIUM, BIG, CATASTROPHIC).

Build a `pomo_stats.csv` with this data, one line per incident

```
filename,title,outage_start,outage_detected,outage_mitigated,outage_ended,root_cause,size
folder/20260101-millennium-bug.md,Millennium Bug hit us!,20260101-09:00:00,,,20260101-12:42:00,HUMAN_ERROR,NEGLIGIBLE
```

## Crunching the data

Once you have the CSV with raw data, you can write some simple code which does the following:

1. Decide what YOUR_DESIGNATED_FOLDER is.
1. Create or Update `POMO_AGGREGATED.md` under YOUR_DESIGNATED_FOLDER/.
1. Caculate for every incident:
   * `outage_duration` (end - start)
   * `time_to_detect` (detect - start)
   * `time_to_mitigate` (mitigate - detect).
   * `detection_rate` (ratio between time_to_detect / outage_duration ). This is indicative of how fast we're to OBSERVE an outage vs FIX it and tells us a lot about our organization.
1. Do an aggregation of all stats except detection_rate (its a percentage on varying numbers, so it's comparing watermellons to cherries).
1. Do a subjective analysis of the detection_rate.
1. Create breakdown by YEAR and PRODUCT.
1. Consider using image generation scripts to create simple graphs.

## Lessons learnt

* See recurring patterns and add a H2 paragraph on `## recurring patterns`: Is there anything we can learn from this aggregation? Is this a mistake we keep on doing? Is there a bug which looks like we're not prioritizing? Is there a number of bugs who all look like the same? This is the step where we can actually identify schemas in this plurality.
* Is there some other lesson we learn from this plurality? Write about it in the `## Conclusions`.
