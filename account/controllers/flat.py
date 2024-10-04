from ninja_extra import api_controller, route,status

from account.schema.flat_schema import FlatCreateSchema, FlatResponseSchema, FlatUpdateSchema
from account.services import FlatService
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth



@api_controller('/flat', tags=["Flats"])
class FlatController:
    
    @route.post('/', response={status.HTTP_201_CREATED: FlatResponseSchema},permissions=[IsAuthenticated], auth=JWTAuth())
    def create_flat(self, payload: FlatCreateSchema):
        """Create a new Flat"""
        flat = FlatService.create_flat(payload)
        return flat

    @route.put('/{flat_id}/', response=FlatResponseSchema)
    def update_flat(self, flat_id: int, payload: FlatUpdateSchema):
        """Update a Flat by its ID"""
        flat = FlatService.update_flat(flat_id, payload)
        return flat

    @route.get('/{flat_id}/', response=FlatResponseSchema)
    def get_flat(self, flat_id: int):
        """Retrieve a Flat by its ID"""
        flat = FlatService.get_flat(flat_id)
        return flat

    @route.delete('/{flat_id}/', response={status.HTTP_204_NO_CONTENT: None})
    def delete_flat(self, flat_id: int):
        """Delete a Flat by its ID"""
        FlatService.delete_flat(flat_id)
        return None

    @route.get('/', response=list[FlatResponseSchema])
    def list_flats(self):
        """List all Flats"""
        return FlatService.list_flats()
    