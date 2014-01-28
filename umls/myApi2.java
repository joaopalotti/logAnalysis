//DEPENDENCY: opencsv and metamap jar must be in your classpath

import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;
import java.io.InputStream;
import java.io.PrintStream;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.DataInputStream;
import java.util.List;
import java.util.ArrayList;
import se.sics.prologbeans.PrologSession;
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.Iterator;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

import au.com.bytecode.opencsv.*;
import gov.nih.nlm.nls.metamap.*;

public class myApi2 {
    /** MetaMap api instance */
    MetaMapApi api;
    Map<String, ArrayList<String> > meshMap; 

    public myApi2() {
        this.api = new MetaMapApiImpl();
        this.meshMap = new HashMap<String, ArrayList<String> >();
        this.readMetaMap();
    }

    /**
     * Creates a new <code>myApi</code> instance using specified host and port.
     *
     * @param serverHostname hostname of MetaMap server.
     * @param serverPort     listening port used by MetaMap server.
     */
    public myApi2(String serverHostname, int serverPort) {
        this.api = new MetaMapApiImpl();
        this.api.setHost(serverHostname);
        this.api.setPort(serverPort);
        
        
        this.meshMap = new HashMap<String, ArrayList<String> >();
        this.readMetaMap();
    }

    public void readMetaMap(){
        System.out.println( "READING MESH FILE ");

        try{
            FileInputStream fstream = new FileInputStream("meshMapComplete");
            BufferedReader br = new BufferedReader(new InputStreamReader(new DataInputStream(fstream)));
            String strLine;
            //Read File Line By Line
            while ((strLine = br.readLine()) != null)   {
                // Print the content on the console

                //System.out.println (strLine);
                String[] s = strLine.split(",");
                if(this.meshMap.containsKey(s[0]) == true){
                    ArrayList<String> al = this.meshMap.get(s[0]);
                    if( al.contains(s[1]) == false){
                        al.add(s[1]);
                    }
                    this.meshMap.put(s[0], al);
                }
                else{
                    ArrayList<String> al = new ArrayList<String>();
                    al.add(s[1]);
                    this.meshMap.put( s[0], al ); 
                
                }

            }
        
		System.out.println( "DONE!");
        }
        catch(java.io.FileNotFoundException e){
            System.out.println( "Mesh file not found! ");
            System.exit(0);
        
        }
        catch(java.io.IOException e){
        }
    }

    void setTimeout(int interval) {
        this.api.setTimeout(interval);
    }


    /**
     * Process terms using MetaMap API and display result to standard output.
     *
     * @param terms input terms
     * @param out output printer
     * @param serverOptions options to pass to metamap server before processing input text.
     */
    List<String> process(String terms, PrintStream out, List<String> serverOptions)  throws Exception
    {
        List<String> toReturn = new ArrayList<String>();

        if (serverOptions.size() > 0) {
            //out.println("Options ==== " + serverOptions);
            api.setOptions(serverOptions);
        }
        if(terms == null || terms.trim().length() == 0)
            return null;
        
        Set<String> mesh = new HashSet<String>();
        Set<String> semantics = new HashSet<String>();
        List<String> posTags = new ArrayList<String>();
        Set<String> sources = new HashSet<String>();
        Set<String> concepts = new HashSet<String>();
        List<Result> resultList = api.processCitationsFromString(terms);
        Map<String,Set<String> > mappingPossibility = new HashMap<String, Set<String> >();

        for (Result result: resultList) {
            if (result != null) {

                //out.println("input text: ");
                //out.println(" " + result.getInputText());
                List<AcronymsAbbrevs> aaList = result.getAcronymsAbbrevsList();
                if (aaList.size() > 0) {
                    out.println("Acronyms and Abbreviations:");
                    for (AcronymsAbbrevs e: aaList) {
                        out.println("Acronym: " + e.getAcronym());
                        out.println("Expansion: " + e.getExpansion());
                        out.println("Count list: " + e.getCountList());
                        out.println("CUI list: " + e.getCUIList());
                    }
                }
                
                List<Negation> negList = result.getNegationList();
                if (negList.size() > 0) {
                    out.println("Negations:");
                    for (Negation e: negList) {
                        out.println("type: " + e.getType());
                        out.print("Trigger: " + e.getTrigger() + ": [");
                        for (Position pos: e.getTriggerPositionList()) {
                            out.print(pos  + ",");
                        }
                        out.println("]");
                        out.print("ConceptPairs: [");
                        for (ConceptPair pair: e.getConceptPairList()) {
                            out.print(pair + ",");
                        }
                        out.println("]");
                        out.print("ConceptPositionList: [");
                        for (Position pos: e.getConceptPositionList()) {
                            out.print(pos + ",");
                        }
                        out.println("]");
                    }
                }

                for (Utterance utterance: result.getUtteranceList()) {
                    /*
                       out.println("Utterance:");
                       out.println(" Id: " + utterance.getId());
                       out.println(" Utterance text: " + utterance.getString());
                       out.println(" Position: " + utterance.getPosition());
                       */
                    
                    
                    for (PCM pcm: utterance.getPCMList()) {
                        String toProcess = pcm.getPhrase().getMincoManAsString();
                        List<String> parsedList = parseList(toProcess);

                        for (int i = 0; i < parsedList.size(); i++) {
                            posTags.add(parsedList.get(i));
                        }

                        /*
                        out.println("Phrase:");
                        out.println(" text: " + pcm.getPhrase().getPhraseText());
                        out.println(" Minimal Commitment Parse: " + pcm.getPhrase().getMincoManAsString());
                        

                        */
                        
                        for (Mapping map: pcm.getMappingList()) {
                            //out.println(" Map Score: " + map.getScore());
                            for (Ev mapEv: map.getEvList()) {
                                
                                //out.println("  Concept Name: " + mapEv.getConceptName());
                                String conceptUID = mapEv.getConceptId();
                                //out.println("  Concept ID: " + conceptUID);
                                concepts.add(conceptUID);

                                
                                String concept = mapEv.getConceptName().toLowerCase();
                                for(String semantic:  mapEv.getSemanticTypes()){
                                    Set<String> myMap = new HashSet<String>();
                                    if (mappingPossibility.containsKey(concept)){
                                        myMap = mappingPossibility.get(concept);
                                    }
                                    myMap.add(semantic);
                                    mappingPossibility.put(concept, myMap);
                                }

                                //Take the MESH code only if the MSH is in the source list
                                if (mapEv.getSources().contains("MSH")){
                                    String conceptId = mapEv.getConceptId();
                                    ArrayList<String> meshIds = this.meshMap.get(conceptId);
                                    if( meshIds != null){
                                        for (String s : meshIds){
                                            //out.println(conceptId + " ---> " + s);
                                            //output += ( s + ";" ) ;
                                            mesh.add(s);
                                        }
                                    }
                                }
                                //output += ( "," ) ;
                                List<String> sourceList = mapEv.getSources();
                                //out.println("  Sources: " + sourceList);
                                for(String s: sourceList){
                                    sources.add(s);
                                }

                                List<String> semanticTypes = mapEv.getSemanticTypes();
                                //out.println("  Semantic Types: " + mapEv.getSemanticTypes());    
                                for(String s: semanticTypes){
                                    //output += (s + ";");
                                    semantics.add(s);
                                }
                                //out.println("  Score: " + mapEv.getScore());
                            }
                        }
                    }
                 }
            } else {
                out.println("NULL result instance! ");
            }
        }

        String output = "";
        if( mesh.size() >= 1){
            Iterator<String> iterator = mesh.iterator();
            String first = iterator.next();
            output += ( first ) ;

            while(iterator.hasNext()) {
                String others = iterator.next();
                output += ( ";" + others ) ;
            }
        }
        toReturn.add(output);
        output = "";

        if( semantics.size() >= 1){
            Iterator<String> iterator = semantics.iterator();
            String first = iterator.next();
            output += ( first ) ;

            while(iterator.hasNext()) {
                String others = iterator.next();
                output += ( ";" + others ) ;
            }
        }
        toReturn.add(output);
        output = "";
         
        if( sources.size() >= 1){
            Iterator<String> iterator = sources.iterator();
            String first = iterator.next();
            output += ( first ) ;

            while(iterator.hasNext()) {
                String others = iterator.next();
                output += ( ";" + others ) ;
            }
        }
        toReturn.add(output);
        output = "";
       
        if( posTags.size() >= 1){
            output += (posTags.get(0));

            for(int i = 1; i < posTags.size(); i++){
                output += ( ";" + posTags.get(i) ) ;
            }
        }
        toReturn.add(output);
        output = "";
        
        if( concepts.size() >= 1){
            Iterator<String> iterator = concepts.iterator();
            String first = iterator.next();
            output += ( first ) ;

            while(iterator.hasNext()) {
                String others = iterator.next();
                output += ( ";" + others ) ;
            }
        }
        toReturn.add(output);
        output = "";
       
        for(Map.Entry<String, Set<String> > entry : mappingPossibility.entrySet()){
            String key = entry.getKey();
            Set<String> values = entry.getValue();
            output = output + key + "|";
            if(values.size() >= 1){
                Iterator<String> it = values.iterator();
                output += it.next();
                while(it.hasNext()){
                    output = output + ";" + it.next();
                }
                output = output + "|";
            }
        }
        out.println(output);
        toReturn.add(output);

        this.api.resetOptions();
        return toReturn;
    }

    public static List<String> parseList(String list) {
    //Parses lists like: [mod([inputmatch([histiocytose]),tag(noun),tokens([histiocytose])]),head([lexmatch([X]),inputmatch([X]),tag(noun),tokens([x])])]
    //Creating another java list: [token, tag]

//        System.out.println("Parsing => " + list);
        List<String> result = new ArrayList<String>();
        int adjust = 0;
        int tokenAdjust = 0;
        //System.out.println("Initial list => " + list);
        Pattern p = Pattern.compile("(tag\\(\\w+\\)|punc|shapes)");
        Matcher m = p.matcher(list);
        while (m.find()) {
            String s = m.group(1);
            if(s.startsWith("tag(")){
                s = s.substring(4, s.length()-1);
            }
            //System.out.println("s --> " + s);
            result.add(s);
        }

        return result;
    }

    public static int countOccurences(String inS, char c){
        
        String s = inS.replaceAll("inputmatch\\(\\[([\\w]*)+[^]]+\\]\\)", "inputmatch\\(\\[a\\]\\)");
//        System.out.println(" newS = "+ s);

        int counter = 0;
        //System.out.println("Counting occurences of "+ c + " in " + s + " (size = " + s.length() + ")");
        for(int i = 0; i < s.length() ; i++){
            if(s.charAt(i) == c){
                counter ++;
                //System.out.println(" i = "+ i );
            }
        }
        return counter;
    }

    public static String getToken(String list){
        return getToken(list, 0);
    }

    public static String getToken(String list, int adjust){
        if(list.isEmpty())
            return null;

        //treat punctuation separately
        if(list.startsWith("punc(")){
            String[] parts = list.split("inputmatch");
            String tag = getElement(parts[1], adjust)[0];
            return tag.substring(2, tag.length() - 2);
        }
        else if(list.startsWith("shapes(")){
            String[] parts = list.split("features");
            String tag = getElement(parts[1])[0];
            return tag.substring(2, tag.length() - 2);
        }

        String[] parts = list.split("tokens\\(");
        if(parts.length != 2){
            System.out.println("TOKEN - Error in the number of parts this string has! Parts: " + parts.length);
            System.out.println("Line => " + list);
            for(int i = 0; i < parts.length; i++){
                System.out.println(i + " --- " + parts[i]);
            }
            System.out.println("Aborting....");
            System.exit(0);
        }
        String token = getElement(parts[1])[0];
        return token.substring(1, token.length() - 2).replaceAll(","," ");

    }

    public static String getTag(String list){
        if(list.isEmpty())
            return null;
        
        //treat punctuation separately
        if(list.startsWith("punc(")){
            return "punc";
        }
        if(list.startsWith("shapes(")){
            return "shape";
        }

        String[] parts = list.split("tag\\(");
        if(parts.length != 2){
            System.out.println("TAG - Error in the number of parts this string has! Parts: " + parts.length);
            System.out.println("Line => " + list);

            for(int i = 0; i < parts.length; i++){
                System.out.println(i + " --- " + parts[i]);
            }

            System.out.println("Aborting....");
            System.exit(0);
        }

        String tag = getElement(parts[1])[0];
        return tag.substring(0, tag.length() - 1);
    }

    public static String[] getElement(String list) {
        return getElement(list, '(', ')', 0);
    }

    public static String[] getElement(String list, int adjust) {
        return getElement(list, '(', ')', adjust);
    }

    public static String[] getElement(String list, char copen, char cclose, int adjust) {
        String result[] = new String[2];
        int start = -1; // counts (
        int stop = -1;
        int count = adjust;
        
        for(int i = 0; i < list.length(); i++){
            if (list.charAt(i) == copen && start == -1){
                start = i;
                count++;
                //System.out.println("Count -> " + count +  "  i = " + i + " charat => " + list.charAt(i));
            }
            else if (list.charAt(i) == copen){
                count++;
                //System.out.println("Count -> " + count +  "  i = " + i + " charat => " + list.charAt(i));
            }
            else if (list.charAt(i) == cclose) {
                count--;
                //System.out.println("Count -> " + count +  "  i = " + i + " charat => " + list.charAt(i));
                if(count <= 0){
                    stop = i;
                    //System.out.println("BREAK! i =  " + i);
                    break;
                }
            }
        }
        result[0] = list.substring(0, stop + 1);
        result[1] = list.substring(stop + 1, list.length());
        return result;
    }


    /** print information about server options */
    public static void printHelp() {
        System.out.println("usage: myApi2 [options]");
        System.out.println("  allowed metamap options: ");
        System.out.println("    -i : input filename ");
        System.out.println("    -o : output filename");
        System.out.println("    -n : number of lines to process.");
        System.out.println("    -a : use it if the process stoped and you want to append the results");
        System.out.println("    -b : metamap will NOT compute abbreviations");
        System.out.println("    -y : metamap will use WSD ");
    }

    /** @param inFile File class referencing input file. */
    static CSVReader readInputFile(String inFileName)  throws java.io.FileNotFoundException, java.io.IOException
    {
        
        System.out.println("Input Filename: " + inFileName.trim());
        CSVReader reader = null;

        if (inFileName.endsWith(".gz")){
            System.out.println("Reading ziped file");
            GZIPInputStream gzip = new GZIPInputStream(new FileInputStream(new File(inFileName.trim())));
            BufferedReader ib = new BufferedReader(new InputStreamReader(gzip));
            reader = new CSVReader(ib, ',', '\"' , '\\');
        }
        else{
            reader = new CSVReader(new FileReader(inFileName), ',', '\"' , '\\');
        }

        return reader;
    }
    
    static ArrayList<String> recoverFail(String outFileName) throws java.io.FileNotFoundException, java.io.IOException{
        
        String lastTime = null;
        String lastUserId = null;
        
        System.out.println("Recoving starts now!!!!! ");
        CSVReader internalReader = new CSVReader(new FileReader(outFileName), ',', '\"' , '\\');
        String[] nextLine;
        String[] previousLine = null;

        while ( (nextLine = internalReader.readNext()) != null) {
            previousLine = nextLine;
        }
        if(previousLine != null){
            lastTime = previousLine[0];
            lastUserId = previousLine[1];
        }
        if(lastTime != null && lastUserId != null){
            System.out.println("Recovered last time = " + lastTime + " and last user id = " + lastUserId);
        }
        
        ArrayList<String> result = new ArrayList<String>();
        result.add(0, lastTime );
        result.add(1, lastUserId);
        return result;
    } 

    public static void main(String[] args) 
        throws Exception
    {
        String serverhost = MetaMapApi.DEFAULT_SERVER_HOST; 
        int serverport = MetaMapApi.DEFAULT_SERVER_PORT; 	// default port
        int timeout = -1; // use default timeout
        String inFilename = null;
        String outFile = "output.csv";
        int totalLines = -1;
        boolean append = false;
        boolean wsd = false;
        HashMap<String, List<String> > cache = new HashMap<String, List<String> >();
        List<String> options = new ArrayList<String>();

        InputStream input = System.in;
        PrintStream output = System.out;
        if (args.length < 1) {
            //    printHelp();
            System.out.println("Enter the filename, please");
            printHelp();
            System.exit(0);
        }
        
        for( int i = 0; i < args.length; i++){
            if ( args[i].equals("-a") ){
                append = true; // it is necessary to write "true"
	            System.out.println("I will try to use the content from the output file" );
            }
            else if(args[i].equals("-n")){
                totalLines = new Integer(args[i+1]);
	            System.out.println("Using information about the number of lines " + totalLines );
            }
            else if(args[i].equals("-o")){
                outFile = args[i+1];
	            System.out.println("Writing output to file " + outFile );
            }
            else if(args[i].equals("-i")){
                inFilename = args[i+1];
	            System.out.println("Input file is " + inFilename);
            }
            else if ( args[i].equals("-b") ){
	            System.out.println("Using abbreviations");
	            options.add("a");
            }
            else if ( args[i].equals("-y") ){
                wsd = true;
                System.out.println("using WSD");
	            options.add("y");
            }
        }
        if(inFilename == null){
	            System.out.println("Error...use -i <filename> to enter the filename you want.");
	            System.exit(0);
        }
        
        // start service
        myApi2 frontEnd = new myApi2(serverhost, serverport);
        System.out.println("options: " + options);
       
        // configure input file
        CSVReader reader = readInputFile(inFilename);

        if (reader == null) {
            System.out.println("File not found. Aborted.");
            System.exit(0);
        }
        
        String lastTime = null;
        String lastUserId = null;
    
        if(append){
            ArrayList<String> timeAndId = recoverFail(outFile);
            lastTime = timeAndId.get(0);
            lastUserId = timeAndId.get(1);
        }

        CSVWriter writer = new CSVWriter(new FileWriter(outFile, append), ',', '\"', '\\');

        String [] nextLine;
        int lineNumber = 0;
        boolean recovered = false;
        
        while ((nextLine = reader.readNext()) != null) {
            
            if(append && !recovered){
                if( nextLine[0].equals(lastTime) && nextLine[1].equals(lastUserId)){
                    recovered = true;
                    continue;
                }
                if(!recovered){
                    lineNumber++;
                    continue;
                }
            }

            //System.out.println(nextLine[0] + "," + nextLine[1] + ", " + nextLine[2] + ", " + nextLine[3] + ", " + nextLine[4]);
            
            String inString = nextLine[2];
            System.out.println("INPUT = " + inString);

            if( inString.matches(".*' s$") ){
                System.out.println("BAD STRING FOUND. Skipping it ---> " + inString);
                lineNumber++;
                continue;
            }
            if( inString.matches("(^|.* )[pP][mM][iI][dD]:.*")){
                System.out.println("BAD STRING FOUND. Skipping it ---> " + inString);
                lineNumber++;
                continue;
            }
            if( inString.matches(" *")){
                System.out.println("BAD STRING FOUND. Skipping it ---> " + inString);
                lineNumber++;
                continue;
            }
            
            List<String> processed = null;

            if ( cache.containsKey(inString) ){
                processed = cache.get(inString);
            }
            else{
                processed = frontEnd.process( inString, output, options);
                cache.put(inString, processed);
            }

            if (processed == null){
                lineNumber++;
                continue;
            }
            
            String [] toWrite = new String [nextLine.length + processed.size() - 2];
           
            // in version 5, we need to write the umls in the positions 4 and 5 (starting the counting from 0)
            int j = 0;

            //Two last cols should be empty strings
            for(  ; j < 4; j++){
                toWrite[j] = nextLine[j]; 
            }
            
            for( int k = 0  ; k  < 2; j++, k++){
                System.out.println(" element ---> " + processed.get(k));
                toWrite[j] = processed.get( k );
            }
            
            for(  ; j < nextLine.length; j++){
                toWrite[j] = nextLine[j]; 
            }
            
            for( int k = 2  ; k  < processed.size()  ; j++, k++){
                System.out.println(" element ---> " + processed.get(k));
                toWrite[j] = processed.get( k );
            }
 
            writer.writeNext(toWrite, false);
            writer.flush();
            lineNumber++;

            if(totalLines < 0){
                System.out.println("PROCESSED LINES ====> " + lineNumber);
            }
            else{
                System.out.printf("PORCENTAGE PROCESSED  ====> %.4f \n\n", 100.0 * lineNumber/totalLines);
            
            }
        }
        
        writer.close();
        reader.close();

        /*
        } else if (termBuf.length() > 0) {
            File inFile = new File(termBuf.toString().trim()); 
            if (inFile.exists()) {
                System.out.println("input file: " + termBuf);
                frontEnd.process(readInputFile(inFile), output, options);
            } else {
                frontEnd.process(termBuf.toString(), output, options);
            }
            frontEnd.api.disconnect();
        } else {
            printHelp();
            System.exit(0);
        }
        */
    }
}
