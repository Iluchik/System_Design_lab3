from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from model.model import Package_description, Package

# ==== Package service ================================================================================================

class package_service():

	async def create_package(self, package_desc: Package_description, current_user: dict, db: Session):
		if package_desc.recipient_id == current_user["user"].id:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't send a package to yourself")
		dictionary = dict(sender_id=current_user["user"].id, recipient_id=package_desc.recipient_id, package_weight=package_desc.package_weight, package_dimensions=package_desc.package_dimensions, package_descriptions=package_desc.package_descriptions)
		db_package = Package(**dictionary)
		db.add(db_package)
		db.commit()
		db.refresh(db_package)
		return db_package

	async def get_user_packages(self, current_user: dict, db: Session):
		return db.query(Package).filter(Package.sender_id == current_user["user"].id).all() + db.query(Package).filter(Package.recipient_id == current_user["user"].id).all()

	async def update_package(self, updated_package: dict, current_user: dict, db: Session):
		package = db.query(Package).filter(Package.product_id == updated_package["product_id"]).first()
		if package is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")
		if (package.sender_id == current_user["user"].id) or (package.recipient_id == current_user["user"].id):
			package.sender_id = updated_package["sender_id"]
			package.recipient_id = updated_package["recipient_id"]
			package.package_weight = updated_package["package_weight"]
			package.package_dimensions = updated_package["package_dimensions"]
			package.package_descriptions = updated_package["package_descriptions"]
			db.commit()
			return package
		else:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can only change package related to the current account")

	async def delete_package(self, product_id: str, current_user: dict, db: Session):
		package = db.query(Package).filter(Package.product_id == product_id).first()
		if package is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")
		if (package.sender_id == current_user["user"].id) or (package.recipient_id == current_user["user"].id):
			db.delete(package)
			db.commit()
			return package
		else:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can only change package related to the current account")

# =====================================================================================================================