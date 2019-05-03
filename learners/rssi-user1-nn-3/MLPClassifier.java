import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
import com.google.gson.Gson;


class MLPClassifier {

    private enum Activation { IDENTITY, LOGISTIC, RELU, TANH, SOFTMAX }

    private class Classifier {
        private String hidden_activation;
        private Activation hidden;
        private String output_activation;
        private Activation output;
        private double[][] network;
        private double[][][] weights;
        private double[][] bias;
        private int[] layers;
    }

    private Classifier clf;

    public MLPClassifier(String file) throws FileNotFoundException {
        String jsonStr = new Scanner(new File(file)).useDelimiter("\\Z").next();
        this.clf = new Gson().fromJson(jsonStr, Classifier.class);
        this.clf.network = new double[this.clf.layers.length + 1][];
        for (int i = 0, l = this.clf.layers.length; i < l; i++) {
            this.clf.network[i + 1] = new double[this.clf.layers[i]];
        }
        this.clf.hidden = Activation.valueOf(this.clf.hidden_activation.toUpperCase());
        this.clf.output = Activation.valueOf(this.clf.output_activation.toUpperCase());
    }

    private double[] compute(Activation activation, double[] v) {
        switch (activation) {
            case LOGISTIC:
                for (int i = 0, l = v.length; i < l; i++) {
                    v[i] = 1. / (1. + Math.exp(-v[i]));
                }
                break;
            case RELU:
                for (int i = 0, l = v.length; i < l; i++) {
                    v[i] = Math.max(0, v[i]);
                }
                break;
            case TANH:
                for (int i = 0, l = v.length; i < l; i++) {
                    v[i] = Math.tanh(v[i]);
                }
                break;
            case SOFTMAX:
                double max = Double.NEGATIVE_INFINITY;
                for (double x : v) {
                    if (x > max) {
                        max = x;
                    }
                }
                for (int i = 0, l = v.length; i < l; i++) {
                    v[i] = Math.exp(v[i] - max);
                }
                double sum = 0.;
                for (double x : v) {
                    sum += x;
                }
                for (int i = 0, l = v.length; i < l; i++) {
                    v[i] /= sum;
                }
                break;
        }
        return v;
    }

    public int predict(double[] neurons) {
        this.clf.network[0] = neurons;

        for (int i = 0; i < this.clf.network.length - 1; i++) {
            for (int j = 0; j < this.clf.network[i + 1].length; j++) {
                for (int l = 0; l < this.clf.network[i].length; l++) {
                    this.clf.network[i + 1][j] += this.clf.network[i][l] * this.clf.weights[i][l][j];
                }
                this.clf.network[i + 1][j] += this.clf.bias[i][j];
            }
            if ((i + 1) < (this.clf.network.length - 1)) {
                this.clf.network[i + 1] = this.compute(this.clf.hidden, this.clf.network[i + 1]);
            }
        }
        this.clf.network[this.clf.network.length - 1] = this.compute(this.clf.output, this.clf.network[this.clf.network.length - 1]);

        if (this.clf.network[this.clf.network.length - 1].length == 1) {
            if (this.clf.network[this.clf.network.length - 1][0] > .5) {
                return 1;
            }
            return 0;
        } else {
            int classIdx = 0;
            for (int i = 0; i < this.clf.network[this.clf.network.length - 1].length; i++) {
                classIdx = this.clf.network[this.clf.network.length - 1][i] > this.clf.network[this.clf.network.length - 1][classIdx] ? i : classIdx;
            }
            return classIdx;
        }
    }

    public static void main(String[] args) throws FileNotFoundException {
        if (args.length > 0 && args[0].endsWith(".json")) {

            // Features:
            double[] features = new double[args.length-1];
            for (int i = 1, l = args.length; i < l; i++) {
                features[i - 1] = Double.parseDouble(args[i]);
            }

            // Parameters:
            String modelData = args[0];

            // Estimators:
            MLPClassifier clf = new MLPClassifier(modelData);

            // Prediction:
            int prediction = clf.predict(features);
            System.out.println(prediction);

        }
    }
}