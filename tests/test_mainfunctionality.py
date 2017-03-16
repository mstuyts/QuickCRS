canvas = iface.mapCanvas()
target_crs = QgsCoordinateReferenceSystem()
target_crs.createFromId( 31370, QgsCoordinateReferenceSystem.EpsgCrsId )
canvas.setDestinationCrs(target_crs)
