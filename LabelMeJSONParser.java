import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/**
 *
 * @author Jugin
 */
public class LabelMeJSONParser {

    public static void main(String[] args) throws IOException {
        List<File> jsonFiles = getJSONFilesRecursive();
        Map<String, Integer> m = new TreeMap<>();
        int counter = 0;

        for (File f : jsonFiles) {
            System.out.println(f.getPath());
            List<String> lines = Files.readAllLines(Paths.get(f.getPath()));
            for (String line : lines) {
                String tmp = line.trim();
                if (tmp.startsWith("\"label\"")) {
                    String key = tmp.split(":")[1].split("\"")[1];
                    Integer val = m.get(key);
                    if (val == null) {
                        val = 0;
                    }
                    m.put(key, val + 1);
                    counter++;
                    if (key.length() > 1) {
                        System.out.println("ooops, there is a problem with: " + key + " in file: " + f.getPath());
                    }
                }
            }
        }
        for (Map.Entry<String, Integer> entry : m.entrySet()) {
            String key = entry.getKey();
            Integer value = entry.getValue();
            System.out.println(key + " - " + value);
        }
        System.out.println("Total: " + counter);
    }

    private static List<File> getJSONFilesRecursive() throws IOException {
        List<File> retVal = null;
        File root = new File("input");
        if (root.exists()) {
            retVal = checkDirectoriesRecursive(root);
        }
        return retVal;
    }

    private static List<File> checkDirectoriesRecursive(File dir) throws IOException {
        List<File> retVal = new ArrayList<>();
        if (dir.isDirectory() == true) {
            File files[] = dir.listFiles();

            for (File f : files) {
                if (f.isDirectory()) {
                    List<File> additionalFiles = checkDirectoriesRecursive(f);
                    retVal.addAll(additionalFiles);
                } else if (f.getName().endsWith(".json")) {
                    retVal.add(f);
                }
            }

        }
        return retVal;
    }

}
