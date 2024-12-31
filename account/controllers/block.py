from ninja_extra import api_controller, route,status
from ninja_extra.permissions import IsAuthenticated

from account.permission import UserWithPermission
from account.schema.block_schema import BlockCreateSchema, BlockResponseSchema, BlockUpdateSchema
from account.services import BlockService
from ninja_jwt.authentication import JWTAuth

@api_controller('/blocks', tags=["Blocks"],permissions=[IsAuthenticated], auth=JWTAuth())
class BlockController:
    
    @route.post('/', response={status.HTTP_201_CREATED: BlockResponseSchema},url_name="create",permissions=[UserWithPermission('account.add_block')])
    def create_block(self, payload: BlockCreateSchema):
        """Create a new Block"""
        block = BlockService.create_block(payload)
        return block

    @route.put('/{block_id}/', response=BlockResponseSchema,url_name="update",permissions=[UserWithPermission('account.change_block')])
    def update_block(self, block_id: int, payload: BlockUpdateSchema):
        """Update a Block by its ID"""
        block = BlockService.update_block(block_id, payload)
        return block

    @route.get('/{block_id}/', response=BlockResponseSchema,url_name="detail",permissions=[UserWithPermission('account.view_block')])
    def get_block(self, block_id: int):
        """Retrieve a Block by its ID"""
        block = BlockService.get_block(block_id)
        return block

    @route.delete('/{block_id}/', response={status.HTTP_204_NO_CONTENT: None},url_name="delete",permissions=[UserWithPermission('account.delete_block')])
    def delete_block(self, block_id: int):
        """Delete a Block by its ID"""
        BlockService.delete_block(block_id)
        return None

    @route.get('/', response=list[BlockResponseSchema],url_name="list",permissions=[UserWithPermission('account.view_block')])
    def list_blocks(self):
        """List all Blocks"""
        return BlockService.list_blocks()
