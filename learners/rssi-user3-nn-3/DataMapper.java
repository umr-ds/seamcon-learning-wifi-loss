package de.uni_marburg.ds.seamlesslogger.learner;

import java.util.List;
import java.util.Map;

public class DataMapper {
static double[] map(Map<String, SensorObject> sensors) throws Classifier.SensorMissingException, Classifier.ObservationWindowException {
    Classifier.ObservationWindowException observationWindowException = null;
    SensorObject sensorObject;
    List readings;
        double[] features = new double[60];

        sensorObject = sensors.get("WIFI_DATA_RSSI");
        if (sensorObject == null) throw new Classifier.SensorMissingException("WIFI_DATA_RSSI");
        readings = sensorObject.getReadings();
        if (readings.size() < 60) observationWindowException = new Classifier.ObservationWindowException("WIFI_DATA_RSSI", 60-readings.size());
        else { 
            features[0] = ((double) readings.get(59) - -51.22312917316746) / 13.05953372515126;
            features[1] = ((double) readings.get(58) - -51.22312917316746) / 13.05953372515126;
            features[2] = ((double) readings.get(57) - -51.22312917316746) / 13.05953372515126;
            features[3] = ((double) readings.get(56) - -51.22312917316746) / 13.05953372515126;
            features[4] = ((double) readings.get(55) - -51.22312917316746) / 13.05953372515126;
            features[5] = ((double) readings.get(54) - -51.22312917316746) / 13.05953372515126;
            features[6] = ((double) readings.get(53) - -51.22312917316746) / 13.05953372515126;
            features[7] = ((double) readings.get(52) - -51.22312917316746) / 13.05953372515126;
            features[8] = ((double) readings.get(51) - -51.22312917316746) / 13.05953372515126;
            features[9] = ((double) readings.get(50) - -51.22312917316746) / 13.05953372515126;
            features[10] = ((double) readings.get(49) - -51.22312917316746) / 13.05953372515126;
            features[11] = ((double) readings.get(48) - -51.22312917316746) / 13.05953372515126;
            features[12] = ((double) readings.get(47) - -51.22312917316746) / 13.05953372515126;
            features[13] = ((double) readings.get(46) - -51.22312917316746) / 13.05953372515126;
            features[14] = ((double) readings.get(45) - -51.22312917316746) / 13.05953372515126;
            features[15] = ((double) readings.get(44) - -51.22312917316746) / 13.05953372515126;
            features[16] = ((double) readings.get(43) - -51.22312917316746) / 13.05953372515126;
            features[17] = ((double) readings.get(42) - -51.22312917316746) / 13.05953372515126;
            features[18] = ((double) readings.get(41) - -51.22312917316746) / 13.05953372515126;
            features[19] = ((double) readings.get(40) - -51.22312917316746) / 13.05953372515126;
            features[20] = ((double) readings.get(39) - -51.22312917316746) / 13.05953372515126;
            features[21] = ((double) readings.get(38) - -51.22312917316746) / 13.05953372515126;
            features[22] = ((double) readings.get(37) - -51.22312917316746) / 13.05953372515126;
            features[23] = ((double) readings.get(36) - -51.22312917316746) / 13.05953372515126;
            features[24] = ((double) readings.get(35) - -51.22312917316746) / 13.05953372515126;
            features[25] = ((double) readings.get(34) - -51.22312917316746) / 13.05953372515126;
            features[26] = ((double) readings.get(33) - -51.22312917316746) / 13.05953372515126;
            features[27] = ((double) readings.get(32) - -51.22312917316746) / 13.05953372515126;
            features[28] = ((double) readings.get(31) - -51.22312917316746) / 13.05953372515126;
            features[29] = ((double) readings.get(30) - -51.22312917316746) / 13.05953372515126;
            features[30] = ((double) readings.get(29) - -51.22312917316746) / 13.05953372515126;
            features[31] = ((double) readings.get(28) - -51.22312917316746) / 13.05953372515126;
            features[32] = ((double) readings.get(27) - -51.22312917316746) / 13.05953372515126;
            features[33] = ((double) readings.get(26) - -51.22312917316746) / 13.05953372515126;
            features[34] = ((double) readings.get(25) - -51.22312917316746) / 13.05953372515126;
            features[35] = ((double) readings.get(24) - -51.22312917316746) / 13.05953372515126;
            features[36] = ((double) readings.get(23) - -51.22312917316746) / 13.05953372515126;
            features[37] = ((double) readings.get(22) - -51.22312917316746) / 13.05953372515126;
            features[38] = ((double) readings.get(21) - -51.22312917316746) / 13.05953372515126;
            features[39] = ((double) readings.get(20) - -51.22312917316746) / 13.05953372515126;
            features[40] = ((double) readings.get(19) - -51.22312917316746) / 13.05953372515126;
            features[41] = ((double) readings.get(18) - -51.22312917316746) / 13.05953372515126;
            features[42] = ((double) readings.get(17) - -51.22312917316746) / 13.05953372515126;
            features[43] = ((double) readings.get(16) - -51.22312917316746) / 13.05953372515126;
            features[44] = ((double) readings.get(15) - -51.22312917316746) / 13.05953372515126;
            features[45] = ((double) readings.get(14) - -51.22312917316746) / 13.05953372515126;
            features[46] = ((double) readings.get(13) - -51.22312917316746) / 13.05953372515126;
            features[47] = ((double) readings.get(12) - -51.22312917316746) / 13.05953372515126;
            features[48] = ((double) readings.get(11) - -51.22312917316746) / 13.05953372515126;
            features[49] = ((double) readings.get(10) - -51.22312917316746) / 13.05953372515126;
            features[50] = ((double) readings.get(9) - -51.22312917316746) / 13.05953372515126;
            features[51] = ((double) readings.get(8) - -51.22312917316746) / 13.05953372515126;
            features[52] = ((double) readings.get(7) - -51.22312917316746) / 13.05953372515126;
            features[53] = ((double) readings.get(6) - -51.22312917316746) / 13.05953372515126;
            features[54] = ((double) readings.get(5) - -51.22312917316746) / 13.05953372515126;
            features[55] = ((double) readings.get(4) - -51.22312917316746) / 13.05953372515126;
            features[56] = ((double) readings.get(3) - -51.22312917316746) / 13.05953372515126;
            features[57] = ((double) readings.get(2) - -51.22312917316746) / 13.05953372515126;
            features[58] = ((double) readings.get(1) - -51.22312917316746) / 13.05953372515126;
            features[59] = ((double) readings.get(0) - -51.22312917316746) / 13.05953372515126;
        }
        if (observationWindowException != null) throw observationWindowException;        
        return features;
    }
}
