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

# DS = ClassificationDataSet(inputdim, nb_classes=2, class_labels=[]);
DS = ClassificationDataSet(9, nb_classes=1, class_labels=["Blue team won", "Red team won"]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], [0]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);
DS.appendLinked([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ], [1]);

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

fnn = buildNetwork( trndata.indim, 9, trndata.outdim, outclass=TanhLayer, hiddenclass=TanhLayer )

trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

# ticks = arange(-3.,6.,0.2)
# X, Y = meshgrid(ticks, ticks)
# # need column vectors in dataset, not arrays
# griddata = ClassificationDataSet(9, nb_classes=1)
# for i in xrange(X.size):
#     griddata.addSample([X.ravel()[i],Y.ravel()[i]], [0])
# griddata._convertToOneOfMany()  # this is still needed to make the fnn feel comfy

for i in range(20):
    trainer.trainEpochs(50)
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
print "activated with 1: "
print fnn.activate([ 1, 1, 1, 1, 1, 1, 1, 1, 1 ]);
print "activated with 0: "
print fnn.activate([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]);
print "activated with -1: "
print fnn.activate([-1, -1, -1, -1, -1, -1, -1, -1, ]);
# ioff()
# show()