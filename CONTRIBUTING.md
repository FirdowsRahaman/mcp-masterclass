# Contributing to MCP Masterclass

Thank you for considering contributing to this repository! This guide outlines the process for submitting improvements and maintaining consistency across the project.

## 🧩 Contribution Types

We welcome contributions in these areas:

- **Content Improvements**: Fixing errors, enhancing explanations, adding examples
- **Lab Exercises**: Creating new labs or improving existing ones
- **Project Implementations**: Contributing real-world project examples
- **Documentation**: Improving READMEs, ROADMAP, or other docs
- **Design Patterns**: Adding new patterns to the design patterns section

## 📝 Contribution Process

1. **Fork the Repository**
   - Click 'Fork' in the top-right corner of this repository

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/descriptive-name
   ```

3. **Make Your Changes**
   - Follow the [Chapter Template](#chapter-template-standards)
   - Ensure examples are tested and working
   - Update relevant documentation

4. **Commit Your Changes**
   ```bash
   git commit -m "feat: add detailed explanation of MCP handshake"
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feature/descriptive-name
   ```

6. **Create a Pull Request**
   - Reference any related issues
   - Include screenshots of changes where applicable
   - Tag the appropriate level (🟢/🟡/🔴)

## 📐 Chapter Template Standards

All chapter content must follow this structure:

```markdown
# Chapter X: Title

## Objective
In 5–10 minutes, you will understand...

## The Concept
- Simple explanation
- Analogy (MANDATORY)
- Diagram reference

## How It Works
- Step-by-step flow
- Sequence explanation

## Code Example
- Minimal working snippet
- Clean + commented

## Try It Yourself
- Step-by-step lab instruction
- Expected output

## Checkpoint
- 1–2 conceptual questions

## Architect Notes
- Trade-offs
- Production considerations
```

## 🏷️ Commit Message Guidelines

Use conventional commits:

- `feat:` for new content or features
- `fix:` for corrections
- `docs:` for documentation changes
- `refactor:` for structural improvements

Example: `feat(chapter-3): add detailed handshake sequence diagram`

## Testing Requirements

- All code examples must be verified working
- Lab instructions must be tested on clean environment
- Diagrams must be updated when concepts change

## 🌐 Community Guidelines

- Be respectful of different learning paces
- Assume positive intent in all communications
- Provide constructive feedback
- Recognize the different mastery levels (🟢/🟡/🔴)

## 📬 Questions?

Open an issue with the `question` label if you're unsure about contribution requirements.