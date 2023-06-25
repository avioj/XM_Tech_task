from pydantic import BaseModel


class OrderRequestDTO(BaseModel):
    stocks: str
    quantity: float


class OrderResponseDTO(OrderRequestDTO):
    id: str
    quantity: float
    status: str  # TODO: enum
    stocks: str
