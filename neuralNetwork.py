from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.structure.modules   import SigmoidLayer
from pybrain.structure.modules   import TanhLayer
from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
import csv

# DS = ClassificationDataSet(inputdim, nb_classes=2, class_labels=[]);
DS = ClassificationDataSet(7, nb_classes=1, class_labels=["Blue team won", "Red team won"]);

with open('game2.csv', 'rb') as csvfile:
    matchReader = csv.reader(csvfile)
    for matchData in matchReader:
        inputList = []
        outputList = []
        i = 0
        for value in matchData:
            if i < 7:
                inputList.append(float(value))
                i += 1
            else:
                outputList.append(float(value))
        DS.appendLinked(inputList,outputList)
        # print matchData
        # print inputList
        # print outputList
csvfile.close()

# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
# DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);

# means = [(-1,0),(2,4),(3,1)]
# cov = [diag([1,1]), diag([0.5,1.2]), diag([1.5,0.7])]
# alldata = ClassificationDataSet(2, 1, nb_classes=3)
# for n in xrange(400):
#     for klass in range(3):
#         input = multivariate_normal(means[klass],cov[klass])
#         alldata.addSample(input, [klass])

# tstdata, trndata = alldata.splitWithProportion( 0.25 )
tstdata, trndata = DS.splitWithProportion(0.2);

# trndata._convertToOneOfMany( )
# tstdata._convertToOneOfMany( )

print "Number of training patterns: ", len(trndata)
print "Input and output dimensions: ", trndata.indim, trndata.outdim
print "First sample (input, target, class):"
print trndata['input'][0], trndata['target'][0]
# print trndata['input'][0], trndata['target'][0], trndata['class'][0]

fnn = buildNetwork( trndata.indim, 7, trndata.outdim, outclass=TanhLayer, hiddenclass=TanhLayer )

trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

# ticks = arange(-3.,6.,0.2)
# X, Y = meshgrid(ticks, ticks)
# # need column vectors in dataset, not arrays
# griddata = ClassificationDataSet(9, nb_classes=1)
# for i in xrange(X.size):
#     griddata.addSample([X.ravel()[i],Y.ravel()[i]], [0])
# griddata._convertToOneOfMany()  # this is still needed to make the fnn feel comfy

for i in range(10):
    trainer.trainEpochs(5)
    # trainer.trainUntilConvergence();
    trnresult = percentError( trainer.testOnClassData(),
                              trndata['class'] )
    tstresult = percentError( trainer.testOnClassData(
           dataset=tstdata ), tstdata['class'] )

    print "epoch: %4d" % trainer.totalepochs, \
          "  train error: %5.2f%%" % trnresult, \
          "  test error: %5.2f%%" % tstresult
#     out = fnn.activateOnDataset(griddata)
#     out = out.argmax(axis=1)  # the highest output activation gives the class
#     out = out.reshape(X.shape)
#     figure(1)
#     ioff()  # interactive graphics off
#     clf()   # clear the plot
#     hold(True) # overplot on
#     for c in [0,1,2]:
#         here, _ = where(tstdata['class']==c)
#         plot(tstdata['input'][here,0],tstdata['input'][here,1],'o')
#     if out.max()!=out.min():  # safety check against flat field
#         contourf(X, Y, out)   # plot the contour
#     ion()   # interactive graphics on
#     draw()  # update the plot
# print "activated with 1: "
# print fnn.activate([ 1.05625511876, -1.01214558617, 0, 3, 1.2, 0, 0]);
# print fnn.activate([1.01797352908, -1.0050781639, -2, 5.0, -1.06349206349, 0, 0])
# print fnn.activate([1.10824090973, 1.15620422232, -1.0, 1.66666666667, 3.85416666667, 0, 0])
# print fnn.activate([1.34279191994, 1.33590398725, -2, 3.5, 1.10769230769, 1, 0])
# print fnn.activate([1.20972364381, 1.23054261441, 1, 4.0, 1.24489795918, 0, 0])
# print "activated with -1: "
# print fnn.activate([-1.28338409646, -1.29251670478, -1, -1.2, -1.68421052632, -1, -1]);
# print fnn.activate([-1.07603764642, -1.00516437839, -2, -1.66666666667, -1.5593220339, 0, 0] )
# print fnn.activate([-1.29981947286, -1.15545164462, 0, -1.33333333333, -1.80434782609, 0, -1])
# print fnn.activate([1.00849382971, -1.05156080837, -2, 1.5, 1.01754385965, 0, 0])
# print fnn.activate([-1.49913637729, -1.40098021952, -1, -1.0, -1.07777777778, 0, -1])
# ioff()
# show()