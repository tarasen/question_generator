
import py4j.GatewayServer;

import java.io.File;
import java.net.URL;

import org.maltparser.concurrent.ConcurrentMaltParserModel;
import org.maltparser.concurrent.ConcurrentMaltParserService;
import org.maltparser.concurrent.graph.ConcurrentDependencyGraph;
import org.maltparser.concurrent.graph.ConcurrentDependencyNode;

public class MaltGateway {

	ConcurrentDependencyGraph outputGraph = null;
	ConcurrentMaltParserModel model = null;

    public MaltGateway(File model_file) {
		try {
			URL url = model_file.toURI().toURL();
			model = ConcurrentMaltParserService.initializeParserModel(url);
		} catch (Exception e) {
			e.printStackTrace();
		}
    }

    private String addedColumnsString(ConcurrentDependencyGraph graph) {
        // Extract columns 6 to 9 as a string
        final StringBuilder sb = new StringBuilder();
        for (int i = 1; i < graph.nTokenNodes(); i++) {
            ConcurrentDependencyNode node = graph.getTokenNode(i);
            sb.append(node.getHeadIndex());
            for (int j = 7; j <= 9; j++) {
                sb.append('\t');
                sb.append(node.getLabel(j));
            }
            sb.append('\n');
        }
        return sb.toString();
    }

    public String[] parseMany(String[] sentences) {
        // TODO: multithreading?
		
		//for(String s: sentences)
		//	System.out.println(s);
		
        String[] out = new String[sentences.length];
        for (int i = 0; i < sentences.length; i++)
        	out[i] = addedColumnsString(parse(sentences[i].split("\n")));
        return out;
    }

    public ConcurrentDependencyGraph parse(String[] tokens) {
        try {
			return model.parse(tokens);
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}
    }

    public static void main(String[] args) {
    	if (args.length < 1 || args.length > 1) {
    		System.out.println("Expected 1 arg: model path (without .mco)");
    		System.exit(1);
    	}
        System.out.println("Loading model from " + args[0] + ".mco");
        GatewayServer gatewayServer = new GatewayServer(new MaltGateway(new File(args[0] + ".mco")));
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }

}

