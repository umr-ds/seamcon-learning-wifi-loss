import sys, os, dill
from sklearn_porter import Porter
from slugify import slugify

import seamless.learning

def _export_mapper(learner, out=sys.stdout):
    '''Transpile a mapper to java'''
    out.write('''package de.uni_marburg.ds.seamlesslogger.learner;

import java.util.List;
import java.util.Map;

public class DataMapper {
static double[] map(Map<String, SensorObject> sensors) throws Classifier.SensorMissingException, Classifier.ObservationWindowException {
    Classifier.ObservationWindowException observationWindowException = null;
    SensorObject sensorObject;
    List readings;\n''')
    out.write("        double[] features = new double[{}];\n".format(len(learner._mapper.features) - 1))

    neuron = 0
    current_readings = ""
    for name, scaler in learner._mapper.features:
        if not scaler: continue
        i = name[0].split("_")[-1]
        sensor_name = "_".join(name[0].split("_")[:-1])
        
        if current_readings != sensor_name:
            if current_readings != "":
                out.write("        }\n")
            out.write("\n        sensorObject = sensors.get(\"{}\");\n".format(sensor_name))
            out.write("        if (sensorObject == null) throw new Classifier.SensorMissingException(\"{}\");\n".format(sensor_name))
            out.write("        readings = sensorObject.getReadings();\n")
            out.write("        if (readings.size() < 60) observationWindowException = new Classifier.ObservationWindowException(\"{}\", 60-readings.size());\n".format(sensor_name))
            out.write("        else { \n")
            current_readings = sensor_name
        
        
        x = "readings.get({})".format(i)
        z = "features[{}]".format(neuron)
    
        out.write("            {};\n".format(_gen_StandardScaler(scaler, x, z)))
        neuron += 1
        
    out.write("        }\n")
    out.write("        if (observationWindowException != null) throw observationWindowException;")
    out.write("        \n")
    out.write("        return features;\n")
    out.write("    }\n}\n")
        
    
def _gen_StandardScaler(scaler, x, z):
    '''express a StandardScaler in java.'''
    return "{z} = ((double) {x} - {mean}) / {scale}".format(x=x, z=z, mean=scaler.mean_[0], scale=scaler.scale_[0])


def export_learner(learner, folder="learners"):
    '''Export transpiled java and python dill dump for a learner.'''
    outfolder = folder + "/" + slugify(learner.codename)

    if not os.path.isdir(outfolder):
        os.makedirs(outfolder)

    with open("{}/MLPClassifier.java".format(outfolder), "w") as f:
        porter = Porter(learner.classifier, language='java')
        f.write(porter.export(export_data=True, export_dir=outfolder))
        
    with open("{}/DataMapper.java".format(outfolder), "w") as f:
        _export_mapper(learner, out=f)

    with open("{}/learner.dill".format(outfolder), "wb") as f:
        dill.dump({k: v for k, v in learner.__dict__.items() if not k.startswith('_Learner__')}, f)


def load_learner(path):
    '''Load a picked learner from a given path.'''
    with open("{}/learner.dill".format(path), "rb") as f:
        learner = seamless.learning.Learner()
        learner.__dict__.update(dill.load(f))
        
    return learner