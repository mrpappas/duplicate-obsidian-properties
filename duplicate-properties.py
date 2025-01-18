import os
import yaml


def process_note(filepath):
    """
    Processes a single Markdown note: parses the YAML frontmatter, formats it as rendered Markdown,
    and appends it to the note body without replacing the original YAML.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split frontmatter and body
    if content.startswith('---'):
        parts = content.split('---', 2)
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
    else:
        print(f"No frontmatter found in {filepath}")
        return

    # Build rendered properties
    rendered_properties = []

    # Render tags as inline hashtags, with error checking
    if 'tags' in frontmatter:
        if isinstance(frontmatter['tags'], list) and frontmatter['tags']:
            tags = ' '.join([f"#{tag}" for tag in frontmatter['tags']])
            rendered_properties.append(tags)
        else:
            print(f"Invalid or empty tags in {filepath}, skipping tags rendering.")

    # Render other properties
    for key, value in frontmatter.items():
        if key == 'tags':  # Skip tags, already rendered
            continue

        # Format property name: replace underscores with spaces and capitalize each word
        formatted_key = key.replace('_', ' ').title()

        # Process value
        if isinstance(value, list):
            value = ', '.join(value)
        elif isinstance(value, str):
            if value.startswith('[[') and value.endswith(']]'):
                # Keep existing Obsidian-style links intact
                pass
            elif value.startswith('http://') or value.startswith('https://'):
                # Leave URLs as they are
                pass
            else:
                # Leave plain text for non-links
                pass

        rendered_properties.append(f"**{formatted_key}:** {value}")

    # Combine properties and body
    rendered_text = '\n'.join(rendered_properties)
    new_content = f"---\n{parts[1]}---\n\n{rendered_text}\n\n{body}"

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(new_content)

    print(f"Processed {filepath}")


def process_folder(folder_path):
    """
    Processes all Markdown notes in the given folder (and subfolders).
    """
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.md'):
                process_note(os.path.join(root, file))


if __name__ == "__main__":
    # Specify the folder containing your Markdown notes
    folder_path = input("Enter the path to the folder with your Markdown notes: ").strip()
    if os.path.isdir(folder_path):
        process_folder(folder_path)
        print("All notes processed.")
    else:
        print(f"Invalid folder path: {folder_path}")
