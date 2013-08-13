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

        List<Result> resultList = api.processCitationsFromString(terms);
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
                        /*
                        out.println("Phrase:");
                        out.println(" text: " + pcm.getPhrase().getPhraseText());
                        out.println(" Minimal Commitment Parse: " + pcm.getPhrase().getMincoManAsString());
                        
                        out.println("Candidates:");

                        for (Ev ev: pcm.getCandidatesInstance().getEvList()) {
                            out.println(" Candidate:");
                            out.println("  Score: " + ev.getScore());
                            out.println("  Concept Id: " + ev.getConceptId());
                            out.println("  Concept Name: " + ev.getConceptName());
                            out.println("  Preferred Name: " + ev.getPreferredName());
                            out.println("  Matched Words: " + ev.getMatchedWords());
                            out.println("  Semantic Types: " + ev.getSemanticTypes());
                            out.println("  MatchMap: " + ev.getMatchMap());
                            out.println("  MatchMap alt. repr.: " + ev.getMatchMapList());
                            out.println("  is Head?: " + ev.isHead());
                            out.println("  is Overmatch?: " + ev.isOvermatch());
                            out.println("  Sources: " + ev.getSources());
                            out.println("  Positional Info: " + ev.getPositionalInfo());
                            out.println("  Pruning Status: " + ev.getPruningStatus());
                        }

                        out.println("Mappings:");
                        */

                        for (Mapping map: pcm.getMappingList()) {
                            //out.println(" Map Score: " + map.getScore());
                            for (Ev mapEv: map.getEvList()) {
                                
                                out.println("  Concept Name: " + mapEv.getConceptName());
                        
                                //Take the MESH code only if the MSH is in the source list
                                if ( mapEv.getSources().contains("MSH") ){
                                    String conceptId = mapEv.getConceptId();
                                    ArrayList<String> meshIds = this.meshMap.get(conceptId);
                                    if( meshIds != null){
                                        for (String s : meshIds){
                                            out.println(conceptId + " ---> " + s);
                                            //output += ( s + ";" ) ;
                                            mesh.add(s);
                                        }
                                    }
                                }
                                //output += ( "," ) ;
                                
                                List<String> semanticTypes = mapEv.getSemanticTypes();
                                out.println("  Semantic Types: " + mapEv.getSemanticTypes());    
                                for(String s: semanticTypes){
                                    //output += (s + ";");
                                    semantics.add(s);
                                }
                                //out.println("  Score: " + mapEv.getScore());
                                //out.println("  Concept Id: " + mapEv.getConceptId());
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

        this.api.resetOptions();
        return toReturn;
    }

    /** print information about server options */
    public static void printHelp() {
        System.out.println("usage: gov.nih.nlm.nls.metamap.MetaMapApiTest [options] terms|inputFilename");
        System.out.println("  allowed metamap options: ");
        System.out.println("    -C : use relaxed model ");
        System.out.println("    -A : use strict model ");
        System.out.println("    -d : no derivational variants");
        System.out.println("    -D : all derivational variants");
        System.out.println("    -a : allow Acronym/Abbreviation variants");
        System.out.println("    -K : ignore stop phrases.");
        System.out.println("    -I : allow Large N");
        System.out.println("    -r : threshold ");
        System.out.println("    -i : ignore word order");
        System.out.println("    -Y : prefer multiple concepts");
        System.out.println("    -b : compute/display all mappings");
        System.out.println("    -X : truncate candidates mapping");
        System.out.println("    -y : use WSD ");
        System.out.println("    -z : use term processing ");
        System.out.println("    -o : allow overmatches ");
        System.out.println("    -g : allow concept gaps");
        System.out.println("    -8 : dynamic variant generation");
        System.out.println("    -@ --WSD <hostname> : Which WSD server to use.");
        System.out.println("    -J --restrict_to_sts <semtypelist> : restrict to semantic types");
        System.out.println("    -R --restrict_to_sources <sourcelist> : restrict to sources");
        System.out.println("    -S --tagger <sourcelist> : Which tagger to use.");
        System.out.println("    -V --mm_data_version <name> : version of MetaMap data to use.");
        System.out.println("    -Z --mm_data_year <name> : year of MetaMap data to use.");
        System.out.println("    -k --exclude_sts <semtypelist> : exclude semantic types");
        System.out.println("    -e --exclude_sources <sourcelist> : exclude semantic types");
        System.out.println("    -r --threshold <integer> : Threshold for displaying candidates.");
        System.out.println("API options:");
        System.out.println("    --metamap_server_host <hostname> : use MetaMap server on specified host");
        System.out.println("    --metamap_server_port <port number> : use MetaMap server on specified host");
        System.out.println("    --metamap_server_timeout <interval> : wait for MetaMap server for specified interval.");
        System.out.println("                                          interval of 0 will wait indefinitely.");
        System.out.println("Program options:");
        System.out.println("    --input <filename> : get input from file.");
        System.out.println("    --output <filename> : send output to file.");
    }

    /** @param inFile File class referencing input file. */
    static CSVReader readInputFile(File inFile)  throws java.io.FileNotFoundException, java.io.IOException
    {
        GZIPInputStream gzip = new GZIPInputStream(new FileInputStream(inFile));
        BufferedReader ib = new BufferedReader(new InputStreamReader(gzip));
        CSVReader reader = new CSVReader(ib);

        return reader;
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
        HashMap<String, List<String> > cache = new HashMap<String, List<String> >();

        InputStream input = System.in;
        PrintStream output = System.out;
        if (args.length < 1) {
            //    printHelp();
            System.out.println("Enter the filename, please");
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
        }
        if(inFilename == null){
	            System.out.println("Error...use -i <filename> to enter the filename you want.");
	            System.exit(0);
        }

        //StringBuffer termBuf = new StringBuffer();
        List<String> options = new ArrayList<String>();
        int i = 0; 
        //ADDED MY DEFAULT OPTION
        //options.add("-R");
        //options.add("MSH");
        /*
        while (i < args.length) {

            if (args[i].charAt(0) == '-') {
                if (args[i].equals("-h") || args[i].equals("--help") || args[i].equals("-?")) {
                    printHelp();
                    System.exit(0);
                } else if ( args[i].equals("-%") || args[i].equals("--XML") ) {
                    options.add(args[i]); i++;
                    options.add(args[i]);
                } else if ( args[i].equals("-@") || args[i].equals("--WSD") ) {
                    options.add(args[i]); i++;
                    options.add(args[i]);
                } else if ( args[i].equals("-J") || args[i].equals("--restrict_to_sts") )  {
                    options.add(args[i]); i++;
                    options.add(args[i]);
                } else if ( args[i].equals("-R") || args[i].equals("--restrict_to_sources") ) {
                    options.add(args[i]); i++;
                    options.add(args[i]);
                } else if ( args[i].equals("-S") || args[i].equals("--tagger") ) {
                    options.add(args[i]); i++;
                    options.add(args[i]);
                } else if ( args[i].equals("-V") || args[i].equals("--mm_data_version") ) {
                    options.add(args[i]); i++;
                    options.add(args[i]);
                } else if ( args[i].equals("-Z") || args[i].equals("--mm_data_year") ) {
                    options.add(args[i]); i++;
                    options.add(args[i]);
                } else if ( args[i].equals("-e") || args[i].equals("--exclude_sources") ) {
                    options.add(args[i]); i++;
                    options.add(args[i]);
                } else if ( args[i].equals("-k") || args[i].equals("--exclude_sts") )  {
                    options.add(args[i]); i++;
                    options.add(args[i]);
                } else if ( args[i].equals("-r") || args[i].equals("--threshold") ) {
                    options.add(args[i]); i++;
                    options.add(args[i]);
                } else if ( args[i].equals("--metamap_server_host") ) {
                    i++;
                    serverhost = args[i];
                } else if ( args[i].equals("--metamap_server_port") ) {
                    i++;
                    serverport = Integer.parseInt(args[i]);
                } else if (args[i].equals("--metamap_server_timeout") ) {
                    i++;
                    timeout = Integer.parseInt(args[i]);
                } else if (args[i].equals("--input") ) {
                    i++;
                    inFilename = args[i];
                    System.out.println("output file: " + args[i]);
                } else if (args[i].equals("--output") ) {
                    i++;
                    output = new PrintStream(args[i]);
                    System.out.println("output file: " + args[i]);
                } else {
                    options.add(args[i]);
                }
            } else {
                termBuf.append(args[i]).append(" "); 
            }
            i++;
        }
        */
        //System.out.println("serverport: " + serverport);
        myApi2 frontEnd = new myApi2(serverhost, serverport);
        //System.out.println("options: " + options);
        //System.out.println("terms: " + termBuf);
        /*
        if (timeout > -1) {
            frontEnd.setTimeout(timeout);
        }
        */
        
        
        if (inFilename != null) {
            File inFile = new File(inFilename.trim()); 

            if (inFile.exists()) {
                    
                System.out.println("input file: " + inFilename);
                
                GZIPInputStream gzip = new GZIPInputStream(new FileInputStream(inFile));
                BufferedReader ib = new BufferedReader(new InputStreamReader(gzip));
                CSVReader reader = new CSVReader(ib, ',', '\"' , '\\');

                String lastTime = null;
                String lastUserId = null;

                if(append){
                    
                    System.out.println("Recoving starts now!!!!! ");
                    CSVReader internalReader = new CSVReader(new FileReader(outFile), ',', '\"' , '\\');
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
                    
                    for( int k = 0  ; k  < processed.size(); j++, k++){
                        System.out.println(" element ---> " + processed.get(k));
                        toWrite[j] = processed.get( k );
                    }
                    
                    for(  ; j < nextLine.length; j++){
                        toWrite[j] = nextLine[j]; 
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
            }
            else{
                System.out.println("File not found. Aborted.");
            }
        }
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
