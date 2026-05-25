-- LLENAR TABLA STORE
INSERT INTO Store (StoreID, PostalCode, City, Address, StoreName)
VALUES (1, '31100', 'Chihuahua', 'Periférico de la Juventud 4500', 'Besitos De Nuez Periferico');

INSERT INTO Store (StoreID, PostalCode, City, Address, StoreName)
VALUES (2, '31124', 'Chihuahua', 'Av. Homero', 'Besitos De Nuez Homero');


-- LLENAR TABLA EMPLOYEE
INSERT INTO Employee (EmployeeID, Name, JobPosition, StoreID)
VALUES (101, 'Stefanya', 'Manager', 1);

INSERT INTO Employee (EmployeeID, Name, JobPosition, StoreID)
VALUES (102, 'Erick', 'Cashier', 2);

INSERT INTO Employee (EmployeeID, Name, JobPosition, StoreID)
VALUES (103, 'Paola', 'Cashier', 1);


-- LLENAR TABLA MENU_ITEM
INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (401, 'MazaPlátano', 95.00, 'Helado sabor plátano con topping de cacahuate');

INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (402, 'Mora-Mor', 100.00, 'Helado sabor frutos rojos');

INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (403, 'Cocazo de crema', 110.00, 'Helado sabor coco');

INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (404, 'Choco-Rolo', 115.00, 'Helado sabor chocorol con chocolate y crema');

INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (405, 'Don Churro', 120.00, 'Helado con canela y churro');

INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (406, 'Ensueño tropical', 90.00, 'Helado de naranja servido con frutos');

INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (407, 'Desvelado de Olla', 125.00, 'Helado sabor café de olla');

INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (408, 'Rosa Mexicano', 105.00, 'Helado sabor granada');

INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (409, 'Pasión Roja', 130.00, 'Helado red velvet');

INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (410, 'Choco-Fresa', 115.00, 'Helado de chocolate y fresa');

INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (411, 'Capricho de la Abuela', 135.00, 'Helado de ciruela con fresa con streusel dulce');

INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (412, 'Pica-Mango', 100.00, 'Helado tropical de mango servido con chamoy');

INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (413, 'Taro con Moras', 125.00, 'Helado taro con frutos rojos');

INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (414, 'Dulces Besos', 95.00, 'Helado vainilla dulce con nuez');

INSERT INTO Menu_Item (MenuItemID, Name, Price, Description)
VALUES (415, 'Luna de Octubre', 140.00, 'Helado edición especial de berries');


-- LLENAR TABLA SUNDAE
INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(601, 401, 'Platano', 1, 'Cacahuate', 'Chocolate', 'Cacahuate', 'Caramelo');

INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(602, 402, 'Mora', 1, 'Frutos Rojos', 'Berry Sauce', 'Cereza', 'Jarabe de Frutos Rojos');

INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(603, 403, 'Coco', 1, 'Vainilla', 'Syrup de Piña', 'Coco Tostado', 'Leche Condensada');

INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(604, 404, 'Chocolate', 1, 'Trozos de Chocorol', 'Chocolate oscuro', 'Chispas de Chocolate', NULL);

INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(605, 405, 'Canela', 1, 'Churro', 'Dulce de Leche', 'Trozos de Churro', 'Caramelo');

INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(606, 406, 'Naranja', 0, 'Fruta Tropical', 'Mango Sauce', 'Frutos Secos', 'Gomitas');

INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(607, 407, 'Vainilla', 0, 'Café de Olla', 'Chocolate', 'Canela', 'Jarabe Moka');

INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(608, 408, 'Granada', 0, 'Trozos de Fresa', 'Berry Sauce', 'Cereza', 'Granadina');

INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(609, 409, 'Pastel', 1, 'Red Velvet', 'Chocolate Blanco', 'Chispas de Chocolate Blanco', 'Queso Crema');

INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(610, 410, 'Fresa', 1, 'Brownie', 'Chocolate', 'Fresa', 'Jarabe de Fresa');

INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(611, 411, 'Vainilla', 0, 'Ciruela', 'Fresa', 'Streusel Dulce', NULL);

INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(612, 412, 'Chamoy', 0, 'Mango', 'Tamarindo', 'Tajin', 'Chamoy Liquido');

INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(613, 413, 'Mora', 1, 'Taro', 'Berry Sauce', 'Moras', NULL);

INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(614, 414, 'Vainilla', 1, 'Bombones', 'Caramelo', 'Nueces', NULL);

INSERT INTO Sundae
(CustomID, MenuItemID, Syrup, WhippedCream, Mixeable, SauceTopping, PlaceableTopping, PourableTopping)
VALUES
(615, 415, 'Fresa', 1, 'Berries', 'Blueberry Sauce', 'Frutos Rojos', 'Galleta');

update menu_item
set description ='Helado vainilla dulce con nueces'
where MENUITEMID=414;

update sundae
set placeabletopping= 'Nueces'
where customid=614;


commit;