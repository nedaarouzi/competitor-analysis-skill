# Competitor analysis skill

An open skill that runs a marketing competitor analysis from two inputs: a **company name** and **three competitors**.

For each competitor it reports:

- the advertising they run, and on which platforms
- their approximate budget
- their approximate cost per acquisition
- the messaging and angle of their ads
- whether they run retargeting

It also identifies the gaps and opportunities in the market, and delivers everything as a structured spreadsheet.

The figures are estimates built from public ad-library data. They show direction, not truth. They are very useful for generating ideas and for understanding the messaging competitors use. Give the skill one real number from your own data and the estimates improve.

## Format

The skill follows the open [Agent Skills](https://agentskills.io) format: a folder with a `SKILL.md` file (YAML frontmatter plus Markdown instructions). The skill is plain text. It has no code and no dependencies.

```
skills/competitor-analysis/SKILL.md
AGENTS.md
```

## Install

Copy the `skills/competitor-analysis` folder into the skills folder of your agent.

| Agent | Where it goes |
|---|---|
| Claude (Claude Code) | `~/.claude/skills/` or `.claude/skills/` in your project |
| Claude (claude.ai) | Zip the `competitor-analysis` folder and upload it under Settings, Capabilities, Skills |
| Codex | `~/.agents/skills/` or `.agents/skills/` in your project |
| Any other agent | If it does not support skills, paste `SKILL.md` into the chat or into its project instructions, or point the agent at `AGENTS.md` |

Folder locations differ between tools and change over time, so check your agent's documentation.

## Use

Ask in plain language:

> Run a competitor analysis for Acme. Competitors: Beta, Gamma, Delta.

Optional: add your market, the channel you care about, and one real number from your own data (for example your cost per acquisition).

## Limits

- Estimates only. A person with judgement should check the numbers that matter before real budget moves.
- Quality depends on the agent being able to browse public ad libraries. Where it cannot, it should say so rather than guess.
- Competitor analysis goes out of date quickly. Re-run it regularly.

## Contributing

Improvements are welcome: new sources, extra output tabs, translations. Keep `SKILL.md` short, specific and free of company-confidential data.

## Licence

MIT. See [LICENSE](LICENSE).
