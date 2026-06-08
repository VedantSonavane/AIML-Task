# EDA Analysis Example

## Dataset Overview

### Leads Dataset
- **Records**: 2,000
- **Features**: 9 (lead_id, name, company, segment, company_size, location, source, created_at, converted)
- **Conversion Rate**: 15.5%

### Interactions Dataset
- **Records**: 40,000
- **Features**: 15 (interaction_id, lead_id, session_id, timestamp, page_name, event_type, event_name, duration_seconds, scroll_depth, funnel_stage, utm_source, utm_campaign, device, browser, converted)
- **Unique Sessions**: 10,039
- **Date Range**: 90 days

### Data Quality
- **Missing Values**: 2% (mostly in utm fields)
- **Duplicates**: 0
- **Invalid Timestamps**: 3 rows (removed)
- **Outliers**: 156 rows with scroll_depth > 100% (kept, likely legitimate)

---

## Key Findings

### 1. Conversion by Lead Source

| Source | Count | Conversion Rate | Avg Interactions |
|--------|-------|-----------------|------------------|
| Referral | 450 | 32% | 18.5 |
| Google | 680 | 22% | 14.2 |
| LinkedIn | 320 | 18% | 11.8 |
| Direct | 280 | 12% | 8.3 |
| Ads | 270 | 8% | 5.2 |

**Insight**: Referral leads are 4x more likely to convert than Ads leads.

---

### 2. Session Behavior Analysis

| Metric | Low Converters | High Converters |
|--------|---|---|
| Avg Sessions | 2.3 | 8.5 |
| Avg Session Duration | 145s | 420s |
| Pricing Page Views | 0.4 | 2.8 |
| Demo Requests | 0.05 | 0.6 |
| Return Rate | 22% | 68% |

**Insight**: Converters engage 3-4x more than non-converters.

---

### 3. Behavioral Segments Discovered

#### Segment A: High Intent Buyers (5%)
- Multiple pricing page visits
- Demo requests
- Return visitors (60%+ return rate)
- Conversion: 78%

#### Segment B: Researchers (30%)
- Case study views
- Webinar participation
- Resource downloads
- High engagement, low conversion: 8%

#### Segment C: Window Shoppers (50%)
- Blog readers
- 1-2 sessions
- No pricing page visits
- Conversion: 2%

#### Segment D: Fast Converters (10%)
- Direct to pricing
- Quick decision path
- High conversion: 60%
- Avg 3 sessions

#### Segment E: Bots/Noise (1%)
- 100+ page views
- Tiny session durations (<5s each)
- Never convert

---

### 4. Feature Importance Predictors

**Top 5 Predictive Features**:
1. `demo_request_flag` (importance: 0.25)
2. `pricing_page_views` (importance: 0.22)
3. `session_count` (importance: 0.18)
4. `whatsapp_clicks` (importance: 0.15)
5. `email_opens` (importance: 0.12)

**Insight**: High-intent signals (demo, pricing interest) are strongest predictors.

---

### 5. Temporal Patterns

| Month | Demo Requests | Conversion Rate |
|-------|---|---|
| January | 185 | 18% |
| February | 178 | 17% |
| March | 195 | 19% |
| April | 162 | 14% |
| May | 180 | 16% |

**Insight**: January-March show 25% higher demo activity. Seasonal effect exists.

---

## Anomalies Detected

### Data Quality Issues
- **Future Timestamps**: 3 rows with timestamp > current date
- **Duplicate Sessions**: 8 leads with identical session patterns (likely bots)
- **Missing Funnel Stages**: 1,245 rows missing funnel classification
- **Invalid Devices**: 15 rows with unexpected device types

### Behavioral Anomalies
- **180-Day Cold Leads**: 52 leads created but never visited (0 interactions)
- **Rapid Converters**: 23 leads converted within 30 minutes of landing
- **High-Volume Non-Converters**: 12 leads with 200+ interactions, 0 conversion

---

## Recommendations

### For Product Team
1. Focus on pricing page experience (strongest signal)
2. Create friction for bot-like behavior
3. Improve demo request process
4. Analyze referral source quality

### For Marketing Team
1. Double down on referral channel ROI is 4x better
2. Optimize paid ads (lowest conversion 8%)
3. Create seasonal campaigns around high-intent periods
4. Segment messaging by behavioral type

### For Data Team
1. Implement real-time anomaly detection (bots)
2. Missing funnel stage data needs imputation
3. Track session quality metrics
4. Monitor temporal trends

---

## Limitations & Caveats

- Conversion definition may vary across sources
- Some leads may have external sales interactions (not tracked)
- Attribution model is last-touch (may undervalue awareness)
- Seasonal effects may not persist beyond 90-day window
- Bot detection is heuristic-based (1-2% may be false positives)

---

## Next Steps

1. Feature engineering for ML model
2. Build predictive model on identified segments
3. Validate findings on holdout test set
4. Monitor model performance in production
