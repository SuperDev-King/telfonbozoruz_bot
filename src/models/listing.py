from dataclasses import dataclass
from typing import Optional

@dataclass
class Listing:
    """Represents a phone listing in the marketplace."""
    name: str
    category: str
    description: str
    price: str
    photo_id: str
    username: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Listing':
        """Create a Listing instance from a dictionary."""
        return cls(
            name=data['name'],
            category=data['category'],
            description=data['description'],
            price=data['price'],
            photo_id=data['photo_id'],
            username=data['username']
        )

    def to_dict(self) -> dict:
        """Convert the Listing instance to a dictionary."""
        return {
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'price': self.price,
            'photo_id': self.photo_id,
            'username': self.username
        } 