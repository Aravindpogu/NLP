import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import org.apache.commons.lang3.StringUtils;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Consumer;

import static java.nio.file.Files.newBufferedReader;
import static java.nio.file.Files.newBufferedWriter;
import static java.util.Collections.reverseOrder;
import static java.util.Map.Entry.comparingByKey;
import static org.apache.commons.lang3.StringUtils.countMatches;

/**
 * @author Aravind Pogu
 */
public class POSTagProcessor {

    // map to hold tag frequency
    static Map<String, Long> tagFrequencyMap = new HashMap<>();

    public static void main(String[] args) throws Exception {
        Files.lines(Paths.get("tagsName.txt")).forEach(line -> tagFrequencyMap.put(line, 0l));
        writeToPOSResultFile();
        calculateFrequencies();
        writeToFreqDistribFile();
        evaluateAccuracy();
    }

    private static void writeToPOSResultFile() throws Exception {
        MaxentTagger tagger = new MaxentTagger("models/gate-EN-twitter.model");
        try (BufferedWriter writer = newBufferedWriter(Paths.get("POS_result.txt"))) {
            Files.lines(Paths.get("POS_tagger_input.txt"))
                    .filter(StringUtils::isNotEmpty)
                    .map(line -> tagger.tagString(line).trim())
                    .forEach(getStringConsumer(writer));
        }
    }

    private static void writeToFreqDistribFile() throws IOException {
        try (BufferedWriter writer = newBufferedWriter(Paths.get("POS_tagger_freq_result.txt"))) {
            Comparator<Map.Entry<String, Long>> cmp =
                    Map.Entry.<String, Long>comparingByValue(reverseOrder()).thenComparing(comparingByKey());

            tagFrequencyMap.entrySet().stream()
                    .sorted(cmp)
                    .map(entry -> entry.getKey() + " : " + entry.getValue())
                    .forEach(getStringConsumer(writer));
        }
    }

    private static Consumer<String> getStringConsumer(BufferedWriter writer) {
        return newLine -> {
            try {
                writer.write(newLine + "\n");
            } catch (IOException e) {
                e.printStackTrace();
            }
        };
    }

    private static void calculateFrequencies() throws IOException {
        Files.lines(Paths.get("POS_result.txt"))
                .filter(StringUtils::isNotEmpty)
                .forEach(line -> {
                    for (String tag : tagFrequencyMap.keySet()) {
                        tagFrequencyMap.compute(tag, (k, v) -> v + countMatches(line, tag));
                    }
                });
    }

    private static double evaluateAccuracy() throws IOException {
        int actualCounter = 0;
        int myCounter = 0;

        try (BufferedReader actualBr = newBufferedReader(Paths.get("POS_tagger_output.txt"));
             BufferedReader myBr = newBufferedReader(Paths.get("POS_result.txt"))) {
            String actualLine, myLine;
            while (true) {
                actualLine = actualBr.readLine();
                myLine = myBr.readLine();
                if ((StringUtils.isEmpty(actualLine))) {
                    break;
                } else {
                    if (StringUtils.isEmpty(myLine)) {
                        continue;
                    }
                    if (actualLine.equals(myLine.trim())) {
                        myCounter++;
                    }
                }
                actualCounter++;
            }
        }
        double accuracy = (myCounter / (double) actualCounter) * 100;
        System.out.println(accuracy);
        return accuracy;
    }
}
