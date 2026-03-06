#!/usr/bin/env python3
"""House design assistant.

A lightweight planning tool that turns user requirements into a structured
house-design concept, including style guidance, exterior finishes,
interior finishes, and feature ideas.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict, field
from textwrap import fill
from typing import Dict, List


STYLE_KEYWORDS: Dict[str, List[str]] = {
    "modern": ["modern", "minimal", "clean lines", "glass", "sleek"],
    "farmhouse": ["farmhouse", "rustic", "barn", "country", "cozy"],
    "contemporary": ["contemporary", "open concept", "bright", "bold"],
    "traditional": ["traditional", "classic", "timeless", "formal"],
    "coastal": ["coastal", "beach", "light", "airy", "ocean"],
    "craftsman": ["craftsman", "handmade", "wood", "detail", "broad porch"],
}


STYLE_PACKAGES: Dict[str, Dict[str, List[str]]] = {
    "modern": {
        "exterior": [
            "Standing seam metal roof in charcoal",
            "Smooth stucco with dark fiber-cement accent panels",
            "Black anodized aluminum windows",
        ],
        "interior": [
            "Matte engineered oak flooring",
            "Flat-panel cabinetry in warm walnut and soft white",
            "Large-format porcelain tile in wet areas",
        ],
        "features": [
            "Double-height living room glazing",
            "Hidden pantry wall",
            "Integrated linear fireplace",
        ],
    },
    "farmhouse": {
        "exterior": [
            "Board-and-batten siding in off-white",
            "Gable roof with black architectural shingles",
            "Natural stone skirt at base and porch columns",
        ],
        "interior": [
            "Wide-plank white oak floors",
            "Shaker cabinetry with brass hardware",
            "Apron-front kitchen sink with bridge faucet",
        ],
        "features": [
            "Wrap-around front porch",
            "Mudroom with built-in cubbies",
            "Exposed reclaimed wood ceiling beams",
        ],
    },
    "contemporary": {
        "exterior": [
            "Mixed cladding: fiber-cement, wood-look panels, and stone",
            "Asymmetrical massing with strong horizontal lines",
            "Dark bronze window frames",
        ],
        "interior": [
            "Neutral polished concrete or microcement floors",
            "High-gloss lacquer and veneer cabinet mix",
            "Statement staircase with glass balustrade",
        ],
        "features": [
            "Skylight strip over circulation spine",
            "Flexible home office / guest suite",
            "Smart lighting scenes and occupancy controls",
        ],
    },
    "traditional": {
        "exterior": [
            "Painted brick with stone lintel detailing",
            "Symmetrical façade and multi-light windows",
            "Slate-look roof and classic cornice profile",
        ],
        "interior": [
            "Herringbone wood flooring in main hall",
            "Raised-panel cabinetry",
            "Crown molding and paneled feature walls",
        ],
        "features": [
            "Formal dining room with butler pantry",
            "Library / study with built-ins",
            "Generous foyer with central stair",
        ],
    },
    "coastal": {
        "exterior": [
            "Light horizontal lap siding in sand tone",
            "White trim and composite shutters",
            "Metal roof accents over porches",
        ],
        "interior": [
            "Bleached oak flooring",
            "Soft blue-gray cabinetry accents",
            "Textured handmade-look ceramic backsplash",
        ],
        "features": [
            "Indoor-outdoor sliding wall",
            "Covered lanai with summer kitchen",
            "Window benches for view-focused seating",
        ],
    },
    "craftsman": {
        "exterior": [
            "Tapered porch columns on stone piers",
            "Earth-tone shingle + lap siding combination",
            "Deep overhangs with exposed rafter tails",
        ],
        "interior": [
            "Quarter-sawn oak floors and trim",
            "Built-in benches and bookcases",
            "Artisan tile around fireplace and kitchen",
        ],
        "features": [
            "Defined entry with covered porch",
            "Window seat nooks",
            "Handcrafted millwork and door casings",
        ],
    },
}


@dataclass
class PlotDetails:
    width_m: float
    depth_m: float
    slope: str = "flat"
    climate: str = "temperate"
    orientation: str = "north-facing street"


@dataclass
class UserInputs:
    brief: str
    image_descriptions: List[str] = field(default_factory=list)
    required_rooms: List[str] = field(default_factory=lambda: ["3 bedrooms", "2 bathrooms"])
    plot: PlotDetails = field(default_factory=lambda: PlotDetails(width_m=15, depth_m=30))


@dataclass
class DesignProposal:
    selected_style: str
    style_confidence: str
    exterior_finishes: List[str]
    interior_finishes: List[str]
    suggested_features: List[str]
    site_strategy: List[str]
    room_planning_notes: List[str]


class HouseDesignAssistant:
    def infer_style(self, brief: str, image_descriptions: List[str]) -> str:
        combined = f"{brief} {' '.join(image_descriptions)}".lower()
        scores = {style: 0 for style in STYLE_KEYWORDS}

        for style, keywords in STYLE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in combined:
                    scores[style] += 1

        best_style = max(scores, key=scores.get)
        if scores[best_style] == 0:
            return "contemporary"
        return best_style

    def site_strategy(self, plot: PlotDetails) -> List[str]:
        area = plot.width_m * plot.depth_m
        notes = [
            f"Plot area is approximately {area:.0f} m²; reserve 35-45% for landscaped open space.",
            f"Align main living spaces for {plot.orientation} with controlled glazing for daylight comfort.",
            f"Use a {plot.slope} slope strategy: stepped slab and drainage channels if not flat.",
            f"Specify envelope and shading details suitable for {plot.climate} climate.",
        ]
        return notes

    def room_planning_notes(self, required_rooms: List[str]) -> List[str]:
        joined = ", ".join(required_rooms)
        return [
            f"Prioritize adjacency planning for: {joined}.",
            "Keep kitchen, dining, and family spaces connected; isolate acoustic-sensitive spaces.",
            "Plan storage early: pantry, linen, utility, and integrated wardrobes.",
        ]

    def propose(self, inputs: UserInputs) -> DesignProposal:
        style = self.infer_style(inputs.brief, inputs.image_descriptions)
        package = STYLE_PACKAGES[style]

        confidence = "high" if len(inputs.image_descriptions) > 0 else "medium"

        return DesignProposal(
            selected_style=style,
            style_confidence=confidence,
            exterior_finishes=package["exterior"],
            interior_finishes=package["interior"],
            suggested_features=package["features"],
            site_strategy=self.site_strategy(inputs.plot),
            room_planning_notes=self.room_planning_notes(inputs.required_rooms),
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a detailed house design proposal.")
    parser.add_argument("--brief", required=True, help="Written description of desired house style and goals.")
    parser.add_argument(
        "--images",
        default="",
        help="Comma-separated image descriptors (e.g. 'dark roof, white facade, stone porch').",
    )
    parser.add_argument(
        "--rooms",
        default="3 bedrooms,2 bathrooms,open kitchen,living room",
        help="Comma-separated required rooms/spaces.",
    )
    parser.add_argument("--plot-width", type=float, default=15.0)
    parser.add_argument("--plot-depth", type=float, default=30.0)
    parser.add_argument("--slope", default="flat")
    parser.add_argument("--climate", default="temperate")
    parser.add_argument("--orientation", default="north-facing street")
    parser.add_argument("--json", action="store_true", help="Print output as JSON")
    return parser.parse_args()


def pretty_print(proposal: DesignProposal) -> None:
    print("\nHOUSE DESIGN PROPOSAL")
    print("=" * 72)
    print(f"Style: {proposal.selected_style.title()} (confidence: {proposal.style_confidence})")

    sections = {
        "Exterior Finishes": proposal.exterior_finishes,
        "Interior Finishes": proposal.interior_finishes,
        "Suggested Features": proposal.suggested_features,
        "Site Strategy": proposal.site_strategy,
        "Room Planning Notes": proposal.room_planning_notes,
    }

    for title, items in sections.items():
        print(f"\n{title}:")
        for item in items:
            print(f"  - {fill(item, width=68, subsequent_indent='    ')}")


def main() -> None:
    args = parse_args()
    inputs = UserInputs(
        brief=args.brief,
        image_descriptions=[s.strip() for s in args.images.split(",") if s.strip()],
        required_rooms=[s.strip() for s in args.rooms.split(",") if s.strip()],
        plot=PlotDetails(
            width_m=args.plot_width,
            depth_m=args.plot_depth,
            slope=args.slope,
            climate=args.climate,
            orientation=args.orientation,
        ),
    )

    assistant = HouseDesignAssistant()
    proposal = assistant.propose(inputs)

    if args.json:
        print(json.dumps(asdict(proposal), indent=2))
    else:
        pretty_print(proposal)


if __name__ == "__main__":
    main()
