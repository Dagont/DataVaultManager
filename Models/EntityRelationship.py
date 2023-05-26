from Models.DataVaultEntity import DataVaultEntity


class EntityRelationship:
	def __init__(self, entity1, entity2):
		if not isinstance(entity1, DataVaultEntity) or not isinstance(entity2, DataVaultEntity):
			raise ValueError("Both entities must be instances of the DataVaultEntity class.")

		# Check for valid combinations (Hub+Sat), (Hub+Link), (Link+Sat)
		if not ((entity1.is_hub and entity2.is_sat) or
		        (entity1.is_hub and entity2.is_link) or
		        (entity1.is_link and entity2.is_sat) or
		        (entity2.is_hub and entity1.is_sat) or
		        (entity2.is_hub and entity1.is_link) or
		        (entity2.is_link and entity1.is_sat)):
			raise ValueError("Invalid entity relationship. The relationship can only be (Hub+Sat), (Hub+Link), (Link+Sat).")

		self._entity1 = entity1
		self._entity2 = entity2

	@property
	def entity1(self):
		return self._entity1

	@property
	def entity2(self):
		return self._entity2

	def __repr__(self):
		return f"EntityRelationship(entity1={self._entity1}, entity2={self._entity2})"
