package pkg.view;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.util.Scanner;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import pkg.MainApp;
import pkg.model.DataBase;

public class AppController {

	@FXML
	private Label firstNameLabel;
	@FXML
	private Label lastNameLabel;
	@FXML
	private Label streetLabel;
	@FXML
	private Label postalCodeLabel;
	@FXML
	private Label cityLabel;
	@FXML
	private Label birthdayLabel;
	@FXML
	private TextField textfield;

	// Reference to the main application.
	private MainApp mainApp;

	/**
	 * The constructor. The constructor is called before the initialize()
	 * method.
	 */
	public AppController() {
	}

	/**
	 * Initializes the controller class. This method is automatically called
	 * after the fxml file has been loaded.
	 */
	@FXML
	private void initialize() {
		// Initialize the person table with the two columns.
		// firstNameColumn.setCellValueFactory(cellData ->
		// cellData.getValue().firstNameProperty());
		// lastNameColumn.setCellValueFactory(cellData ->
		// cellData.getValue().lastNameProperty());
	}

	/**
	 * Is called by the main application to give a reference back to itself.
	 * 
	 * @param mainApp
	 */
	public void setMainApp(MainApp mainApp) {
		this.mainApp = mainApp;

		// Add observable list data to the table
		// personTable.setItems(mainApp.getPersonData());
	}

	/**
	 * Called when the user clicks the search button
	 */
	@FXML
	private void handleSearch() {
//		System.out.println(textfield.getText());
		try {
			PrintWriter writer = new PrintWriter("./search/search.txt", "UTF-8");
			writer.println(textfield.getText());
			writer.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
		runPy();
	}

	public void runPy() {

		String s = null;
//		String python_path = null;
		//set the python path accordingly
		try {
			Process p = Runtime.getRuntime().exec("python3 475.py");
			BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
			// read the output from the command
			System.out.println("Here is the standard output of the command:\n");
			while ((s = stdInput.readLine()) != null) {
				System.out.println(s);
			}
			BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));

			
			// read any errors from the attempted command
			System.out.println("Here is the standard error of the command (if any):\n");
			while ((s = stdError.readLine()) != null) {
				System.out.println(s);
			}

		} catch (IOException e) {
			System.out.println("exception happened - here's what I know: ");
			e.printStackTrace();
			System.exit(-1);
		}
	}

	@FXML
	private void handleImport() throws FileNotFoundException {
		Stage stage = new Stage();
		FileChooser fileChooser = new FileChooser();
		fileChooser.setTitle("Open Resource File");
		File file = fileChooser.showOpenDialog(stage);
		// copy the select file in to a create file
		File source = null;
		try {
			source = new File(file.getPath());
		} catch (Exception e) {
			// continue
			// didn't choose file
		}
		String source_name = source.getName();
		File dest = new File(System.getProperty("user.dir") + "/bib_collect/" + source_name);

		try {
			Files.copy(source.toPath(), dest.toPath());
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private static void copyFileUsingStream(File source, File dest) throws IOException {
		InputStream is = null;
		OutputStream os = null;
		try {
			is = new FileInputStream(source);
			os = new FileOutputStream(dest);
			byte[] buffer = new byte[1024];
			int length;
			while ((length = is.read(buffer)) > 0) {
				os.write(buffer, 0, length);
			}
		} finally {
			is.close();
			os.close();
		}
	}

}
