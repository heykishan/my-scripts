---
name: weekday-morning-brief
description: Weekday morning brief: calendar, important unread emails, and items needing attention today.
---

Generate a concise morning brief for Kishan (kishan.baradeswaran@powerverse.com) for today. 

Keep it brief, friendly, and refined in tone. Never use emdashes. Use analogies where they truly clarify.

Pull together the following three sections in this exact order:

1. **Today's Calendar**
   - Use the Google Calendar tools. Always use timeZone: "Asia/Kolkata" (IST, UTC+5:30) — this is Kishan's confirmed local timezone. Display all times in IST.
   - List each event with start time, end time, title, and location/conferencing link if present.
   - Flag any back-to-back meetings or conflicts.
   - If the day is light or empty, say so plainly.

2. **Important Unread Emails**
   - Use Gmail tools to find unread threads from the last 48 hours. Try a query like "is:unread newer_than:1d -category:promotions -category:social".
   - Surface only the ones that look genuinely important: direct messages to the user, threads where the user is named, items from leadership or key collaborators, time-sensitive requests, or threads with action language ("review", "approve", "by EOD", "today", "urgent", etc.).
   - For each, give the sender, subject, and a one-line gist of why it matters.
   - Cap at the top 5 to 7. If none qualify, say the inbox looks quiet.

3. **Jira and Confluence Activity**
- Check my Jira and confluence notifications, tags, to identify what tickets and items I need to action on. Check items broadly from the customer team as well.
   - For each, give the ticket context, and a one-line gist to refresh my memory.

4.**Check my offline Kanban**
- Check my Kanban board at '/Users/kb/Library/Mobile Documents/iCloud~md~obsidian/Documents/all-notes/Work/Work Kanban.md'
- Highlight items due today and overdue issues and if there's any 'Next' items that are coming up or might be relevanet.
- Correlate with any Jira, mail or other items that you find in above steps and contexualise where it makes sense. 

5. **Needs Your Attention Today**
   - Synthesize across the above: deadlines visible in calendar invites or emails, meetings requiring prep, replies owed, action items from Jira and Confluence Activity, Items from my Kanban and any explicit asks with today's date.
   - If a productivity TASKS.md file exists in the user's working memory (check via the productivity:task-management skill context), pull any items due today or overdue.
   - Present as a prioritized list.

Formatting rules:
- For anything you tell me and format the output accordingly
- Open with a one-line greeting and the date.
- Use the five section headers above.
- Keep the whole brief tight: bullets, not paragraphs. Aim for something that can be skimmed in a couple of minutes.
- End with a single closing line that's warm but not effusive.
- Remember to use kevin-speak skill and format the output accordingly


If a connector fails or returns no data, note it briefly under the relevant section and continue with the rest.

Post the digest as a chat message and do not create a file or artifact.
