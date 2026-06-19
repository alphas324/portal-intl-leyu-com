from dataclasses import dataclass, field, asdict
from typing import List, Optional
import json
import textwrap


@dataclass
class KeywordNote:
    keyword: str
    category: str = "general"
    description: str = ""
    reference_url: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    priority: int = 5

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    def formatted_output(self, width: int = 60) -> str:
        lines = []
        lines.append(f"Keyword : {self.keyword}")
        lines.append(f"Category: {self.category}")
        lines.append(f"Priority: {self.priority}")
        lines.append(f"Tags    : {', '.join(self.tags) if self.tags else 'none'}")
        if self.reference_url:
            lines.append(f"URL     : {self.reference_url}")
        if self.description:
            wrapped = textwrap.fill(self.description, width=width)
            for line in wrapped.splitlines():
                lines.append(f"  {line}")
        return "\n".join(lines)


@dataclass
class NoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def all_formatted(self, width: int = 60) -> str:
        blocks = []
        for i, note in enumerate(self.notes, 1):
            header = f"--- Note #{i} ---"
            body = note.formatted_output(width=width)
            blocks.append(f"{header}\n{body}")
        return "\n\n".join(blocks)

    def filter_by_tag(self, tag: str) -> "NoteCollection":
        filtered = [n for n in self.notes if tag in n.tags]
        return NoteCollection(notes=filtered)

    def to_json_all(self) -> str:
        return json.dumps([n.to_dict() for n in self.notes], ensure_ascii=False, indent=2)


def make_sample_notes() -> NoteCollection:
    collection = NoteCollection()
    note1 = KeywordNote(
        keyword="leyu",
        category="entertainment",
        description="Leyu platform offers diverse content for global users.",
        reference_url="https://portal-intl-leyu.com",
        tags=["leyu", "portal", "international"],
        priority=1,
    )
    note2 = KeywordNote(
        keyword="leyu gaming",
        category="gaming",
        description="Gaming features and promotions related to Leyu.",
        reference_url="https://portal-intl-leyu.com/gaming",
        tags=["leyu", "gaming"],
        priority=2,
    )
    note3 = KeywordNote(
        keyword="leyu support",
        category="support",
        description="Customer support contact and FAQ for Leyu users.",
        tags=["leyu", "help"],
        priority=4,
    )
    collection.add(note1)
    collection.add(note2)
    collection.add(note3)
    return collection


def main() -> None:
    collection = make_sample_notes()
    print("=== All Notes (Formatted) ===")
    print(collection.all_formatted(width=50))
    print("\n=== JSON Export ===")
    print(collection.to_json_all())
    print("\n=== Filtered by tag 'help' ===")
    help_notes = collection.filter_by_tag("help")
    print(help_notes.all_formatted())


if __name__ == "__main__":
    main()