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
            features[0] = ((double) readings.get(59) - -54.087888862136815) / 12.941778336058;
            features[1] = ((double) readings.get(58) - -54.087888862136815) / 12.941778336058;
            features[2] = ((double) readings.get(57) - -54.087888862136815) / 12.941778336058;
            features[3] = ((double) readings.get(56) - -54.087888862136815) / 12.941778336058;
            features[4] = ((double) readings.get(55) - -54.087888862136815) / 12.941778336058;
            features[5] = ((double) readings.get(54) - -54.087888862136815) / 12.941778336058;
            features[6] = ((double) readings.get(53) - -54.087888862136815) / 12.941778336058;
            features[7] = ((double) readings.get(52) - -54.087888862136815) / 12.941778336058;
            features[8] = ((double) readings.get(51) - -54.087888862136815) / 12.941778336058;
            features[9] = ((double) readings.get(50) - -54.087888862136815) / 12.941778336058;
            features[10] = ((double) readings.get(49) - -54.087888862136815) / 12.941778336058;
            features[11] = ((double) readings.get(48) - -54.087888862136815) / 12.941778336058;
            features[12] = ((double) readings.get(47) - -54.087888862136815) / 12.941778336058;
            features[13] = ((double) readings.get(46) - -54.087888862136815) / 12.941778336058;
            features[14] = ((double) readings.get(45) - -54.087888862136815) / 12.941778336058;
            features[15] = ((double) readings.get(44) - -54.087888862136815) / 12.941778336058;
            features[16] = ((double) readings.get(43) - -54.087888862136815) / 12.941778336058;
            features[17] = ((double) readings.get(42) - -54.087888862136815) / 12.941778336058;
            features[18] = ((double) readings.get(41) - -54.087888862136815) / 12.941778336058;
            features[19] = ((double) readings.get(40) - -54.087888862136815) / 12.941778336058;
            features[20] = ((double) readings.get(39) - -54.087888862136815) / 12.941778336058;
            features[21] = ((double) readings.get(38) - -54.087888862136815) / 12.941778336058;
            features[22] = ((double) readings.get(37) - -54.087888862136815) / 12.941778336058;
            features[23] = ((double) readings.get(36) - -54.087888862136815) / 12.941778336058;
            features[24] = ((double) readings.get(35) - -54.087888862136815) / 12.941778336058;
            features[25] = ((double) readings.get(34) - -54.087888862136815) / 12.941778336058;
            features[26] = ((double) readings.get(33) - -54.087888862136815) / 12.941778336058;
            features[27] = ((double) readings.get(32) - -54.087888862136815) / 12.941778336058;
            features[28] = ((double) readings.get(31) - -54.087888862136815) / 12.941778336058;
            features[29] = ((double) readings.get(30) - -54.087888862136815) / 12.941778336058;
            features[30] = ((double) readings.get(29) - -54.087888862136815) / 12.941778336058;
            features[31] = ((double) readings.get(28) - -54.087888862136815) / 12.941778336058;
            features[32] = ((double) readings.get(27) - -54.087888862136815) / 12.941778336058;
            features[33] = ((double) readings.get(26) - -54.087888862136815) / 12.941778336058;
            features[34] = ((double) readings.get(25) - -54.087888862136815) / 12.941778336058;
            features[35] = ((double) readings.get(24) - -54.087888862136815) / 12.941778336058;
            features[36] = ((double) readings.get(23) - -54.087888862136815) / 12.941778336058;
            features[37] = ((double) readings.get(22) - -54.087888862136815) / 12.941778336058;
            features[38] = ((double) readings.get(21) - -54.087888862136815) / 12.941778336058;
            features[39] = ((double) readings.get(20) - -54.087888862136815) / 12.941778336058;
            features[40] = ((double) readings.get(19) - -54.087888862136815) / 12.941778336058;
            features[41] = ((double) readings.get(18) - -54.087888862136815) / 12.941778336058;
            features[42] = ((double) readings.get(17) - -54.087888862136815) / 12.941778336058;
            features[43] = ((double) readings.get(16) - -54.087888862136815) / 12.941778336058;
            features[44] = ((double) readings.get(15) - -54.087888862136815) / 12.941778336058;
            features[45] = ((double) readings.get(14) - -54.087888862136815) / 12.941778336058;
            features[46] = ((double) readings.get(13) - -54.087888862136815) / 12.941778336058;
            features[47] = ((double) readings.get(12) - -54.087888862136815) / 12.941778336058;
            features[48] = ((double) readings.get(11) - -54.087888862136815) / 12.941778336058;
            features[49] = ((double) readings.get(10) - -54.087888862136815) / 12.941778336058;
            features[50] = ((double) readings.get(9) - -54.087888862136815) / 12.941778336058;
            features[51] = ((double) readings.get(8) - -54.087888862136815) / 12.941778336058;
            features[52] = ((double) readings.get(7) - -54.087888862136815) / 12.941778336058;
            features[53] = ((double) readings.get(6) - -54.087888862136815) / 12.941778336058;
            features[54] = ((double) readings.get(5) - -54.087888862136815) / 12.941778336058;
            features[55] = ((double) readings.get(4) - -54.087888862136815) / 12.941778336058;
            features[56] = ((double) readings.get(3) - -54.087888862136815) / 12.941778336058;
            features[57] = ((double) readings.get(2) - -54.087888862136815) / 12.941778336058;
            features[58] = ((double) readings.get(1) - -54.087888862136815) / 12.941778336058;
            features[59] = ((double) readings.get(0) - -54.087888862136815) / 12.941778336058;
        }
        if (observationWindowException != null) throw observationWindowException;        
        return features;
    }
}
