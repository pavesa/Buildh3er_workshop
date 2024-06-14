from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)
algorand = AlgorandClient.default_local_net()

dispenser = algorand.account.dispenser()

creator = algorand.account.random()

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)


ent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=1000,
        asset_name="BUILDH3R",
        unit_name="H3R",
        manager=creator.address,
        clawback=creator.address,
        freeze=creator.address
        
    )
)

asset_id = sent_txn["confirmation"]["asset-index"]


receiver_xyz = algorand.account.random()

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver_xyz.address,
        amount=10_000_000
    )
)

group_tx = algorand.new_group()

group_tx.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_xyz.address,
        asset_id=asset_id
    )
)

group_tx.add_payment(
    PayParams(
        sender=receiver_xyz.address,
        receiver=creator.address,
        amount=2_000_000
    )
)

group_tx.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver_xyz.address,
        asset_id=asset_id,
        amount=120
    )
)

group_tx.execute()


print("Receiver Account Asset Balance:", algorand.account.get_information(receiver_xyz.address)['assets'][0]['amount'])
print("Creator Account Asset Balance:", algorand.account.get_information(creator.address)['assets'][0]['amount'])

algorand.send.asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=creator.address,
        asset_id=asset_id,
        amount=3,
        clawback_target=receiver_xyz.address
    )
)

print("Post clawback")

print("Receiver Account Asset Balance:", algorand.account.get_information(receiver_xyz.address)['assets'][0]['amount'])
print("Creator Account Asset Balance:", algorand.account.get_information(creator.address)['assets'][0]['amount'])
