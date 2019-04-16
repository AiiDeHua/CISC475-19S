package pkg.view;


import java.io.File;

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
		String input = textfield.getText();
		System.out.println(input);
	}

	@FXML
	private void handleImport() {
		Stage stage = new Stage();
		FileChooser fileChooser = new FileChooser();
		fileChooser.setTitle("Open Resource File");
		File file = fileChooser.showOpenDialog(stage);
		System.out.println(file.toString());
		
//		JFileChooser chooser = new JFileChooser();
//		FileNameExtensionFilter filter = new FileNameExtensionFilter("JPG & GIF Images", "bib");
//		chooser.setFileFilter(filter);
//		int returnVal = chooser.showOpenDialog(null);
//		if (returnVal == JFileChooser.APPROVE_OPTION) {
//			System.out.println("You chose to open this file: " + chooser.getSelectedFile().getName());
//		}
	
	}
}
