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
            features[0] = ((double) readings.get(59) - -53.27442935165175) / 12.441773784557144;
            features[1] = ((double) readings.get(58) - -53.27442935165175) / 12.441773784557144;
            features[2] = ((double) readings.get(57) - -53.27442935165175) / 12.441773784557144;
            features[3] = ((double) readings.get(56) - -53.27442935165175) / 12.441773784557144;
            features[4] = ((double) readings.get(55) - -53.27442935165175) / 12.441773784557144;
            features[5] = ((double) readings.get(54) - -53.27442935165175) / 12.441773784557144;
            features[6] = ((double) readings.get(53) - -53.27442935165175) / 12.441773784557144;
            features[7] = ((double) readings.get(52) - -53.27442935165175) / 12.441773784557144;
            features[8] = ((double) readings.get(51) - -53.27442935165175) / 12.441773784557144;
            features[9] = ((double) readings.get(50) - -53.27442935165175) / 12.441773784557144;
            features[10] = ((double) readings.get(49) - -53.27442935165175) / 12.441773784557144;
            features[11] = ((double) readings.get(48) - -53.27442935165175) / 12.441773784557144;
            features[12] = ((double) readings.get(47) - -53.27442935165175) / 12.441773784557144;
            features[13] = ((double) readings.get(46) - -53.27442935165175) / 12.441773784557144;
            features[14] = ((double) readings.get(45) - -53.27442935165175) / 12.441773784557144;
            features[15] = ((double) readings.get(44) - -53.27442935165175) / 12.441773784557144;
            features[16] = ((double) readings.get(43) - -53.27442935165175) / 12.441773784557144;
            features[17] = ((double) readings.get(42) - -53.27442935165175) / 12.441773784557144;
            features[18] = ((double) readings.get(41) - -53.27442935165175) / 12.441773784557144;
            features[19] = ((double) readings.get(40) - -53.27442935165175) / 12.441773784557144;
            features[20] = ((double) readings.get(39) - -53.27442935165175) / 12.441773784557144;
            features[21] = ((double) readings.get(38) - -53.27442935165175) / 12.441773784557144;
            features[22] = ((double) readings.get(37) - -53.27442935165175) / 12.441773784557144;
            features[23] = ((double) readings.get(36) - -53.27442935165175) / 12.441773784557144;
            features[24] = ((double) readings.get(35) - -53.27442935165175) / 12.441773784557144;
            features[25] = ((double) readings.get(34) - -53.27442935165175) / 12.441773784557144;
            features[26] = ((double) readings.get(33) - -53.27442935165175) / 12.441773784557144;
            features[27] = ((double) readings.get(32) - -53.27442935165175) / 12.441773784557144;
            features[28] = ((double) readings.get(31) - -53.27442935165175) / 12.441773784557144;
            features[29] = ((double) readings.get(30) - -53.27442935165175) / 12.441773784557144;
            features[30] = ((double) readings.get(29) - -53.27442935165175) / 12.441773784557144;
            features[31] = ((double) readings.get(28) - -53.27442935165175) / 12.441773784557144;
            features[32] = ((double) readings.get(27) - -53.27442935165175) / 12.441773784557144;
            features[33] = ((double) readings.get(26) - -53.27442935165175) / 12.441773784557144;
            features[34] = ((double) readings.get(25) - -53.27442935165175) / 12.441773784557144;
            features[35] = ((double) readings.get(24) - -53.27442935165175) / 12.441773784557144;
            features[36] = ((double) readings.get(23) - -53.27442935165175) / 12.441773784557144;
            features[37] = ((double) readings.get(22) - -53.27442935165175) / 12.441773784557144;
            features[38] = ((double) readings.get(21) - -53.27442935165175) / 12.441773784557144;
            features[39] = ((double) readings.get(20) - -53.27442935165175) / 12.441773784557144;
            features[40] = ((double) readings.get(19) - -53.27442935165175) / 12.441773784557144;
            features[41] = ((double) readings.get(18) - -53.27442935165175) / 12.441773784557144;
            features[42] = ((double) readings.get(17) - -53.27442935165175) / 12.441773784557144;
            features[43] = ((double) readings.get(16) - -53.27442935165175) / 12.441773784557144;
            features[44] = ((double) readings.get(15) - -53.27442935165175) / 12.441773784557144;
            features[45] = ((double) readings.get(14) - -53.27442935165175) / 12.441773784557144;
            features[46] = ((double) readings.get(13) - -53.27442935165175) / 12.441773784557144;
            features[47] = ((double) readings.get(12) - -53.27442935165175) / 12.441773784557144;
            features[48] = ((double) readings.get(11) - -53.27442935165175) / 12.441773784557144;
            features[49] = ((double) readings.get(10) - -53.27442935165175) / 12.441773784557144;
            features[50] = ((double) readings.get(9) - -53.27442935165175) / 12.441773784557144;
            features[51] = ((double) readings.get(8) - -53.27442935165175) / 12.441773784557144;
            features[52] = ((double) readings.get(7) - -53.27442935165175) / 12.441773784557144;
            features[53] = ((double) readings.get(6) - -53.27442935165175) / 12.441773784557144;
            features[54] = ((double) readings.get(5) - -53.27442935165175) / 12.441773784557144;
            features[55] = ((double) readings.get(4) - -53.27442935165175) / 12.441773784557144;
            features[56] = ((double) readings.get(3) - -53.27442935165175) / 12.441773784557144;
            features[57] = ((double) readings.get(2) - -53.27442935165175) / 12.441773784557144;
            features[58] = ((double) readings.get(1) - -53.27442935165175) / 12.441773784557144;
            features[59] = ((double) readings.get(0) - -53.27442935165175) / 12.441773784557144;
        }
        if (observationWindowException != null) throw observationWindowException;        
        return features;
    }
}
