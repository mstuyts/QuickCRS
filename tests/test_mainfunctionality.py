# test for QGIS 2.x
canvas = iface.mapCanvas()
target_crs = QgsCoordinateReferenceSystem()
target_crs.createFromId( 31370, QgsCoordinateReferenceSystem.EpsgCrsId )
canvas.setDestinationCrs(target_crs)

#test for QGIS 3.x
target_crs = QgsCoordinateReferenceSystem()
target_crs.createFromId( 31370, QgsCoordinateReferenceSystem.EpsgCrsId )
QgsProject.instance().setCrs(target_crs)

# Combined test
target_crs = QgsCoordinateReferenceSystem()
target_crs.createFromId( 31370, QgsCoordinateReferenceSystem.EpsgCrsId )
try:
    QgsProject.instance().setCrs(target_crs)
except:
    canvas = iface.mapCanvas()
    canvas.setDestinationCrs(target_crs)
