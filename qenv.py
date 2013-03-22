# Setup the require environmental variables for QSTK
# http://wiki.quantsoftware.org/index.php?title=QuantSoftware_ToolKit
from os import environ
from os.path import join
from sys import path

HOME = '/Users/Aleks'
QS = join(HOME, 'QSTK-0.2.5')
QSDATA = join(HOME, 'QSTK/QSData')

environ.update({
    'QS'             : QS,
    'QSDATA'         : QSDATA,
    'QSDATAPROCESSED': join(QSDATA, 'Processed'),
    'QSDATATMP'      : join(QSDATA, 'Tmp'),
    'QSBIN'          : join(QS, 'Bin'),
    'QSSCRATCH'      : join(QSDATA, 'Scratch'),
    'CACHESTALLTIME' : '12',
})

path.append(QS)