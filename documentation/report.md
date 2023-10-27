# report

### Gebruik van de CSV-module: 

De code maakt gebruik van de CSV-module om gegevens te lezen en schrijven naar CSV-bestanden. Dit is een goede keuze omdat CSV-bestanden een veelvoorkomend formaat zijn voor het opslaan van tabulaire gegevens, en de CSV-module een eenvoudige en efficiënte manier biedt om gegevens naar deze bestanden te lezen en schrijven. De code gebruikt ook de csv.writerows() methode om meerdere rijen tegelijk naar een CSV-bestand te schrijven, wat efficiënter is dan elke rij afzonderlijk schrijven.

### Gebruik van de datetime-module: 

De code maakt gebruik van de datetime-module om met datums en tijden te werken. Dit is een goede keuze omdat de datetime-module een uitgebreide reeks functies biedt voor het werken met datums en tijden, waaronder het analyseren en formatteren van datums, rekenkundige bewerkingen met datums en het omzetten tussen tijdzones. De code gebruikt ook de strftime() methode om datums als strings te formatteren, wat een veelvoorkomende en handige manier is om met datums in Python te werken.

### Gebruik van de tabulate-module: 

De code maakt gebruik van de tabulate-module om opgemaakte tabellen te genereren op basis van gegevens. Dit is een goede keuze omdat opgemaakte gegevens gemakkelijker te lezen en te begrijpen zijn dan ruwe gegevens, vooral bij het werken met grote datasets. De code gebruikt ook het tablefmt argument om het formaat van de tabel op te geven, wat aanpassing van het uiterlijk van de tabel mogelijk maakt. Bovendien exporteert de code de gegenereerde tabel naar een CSV-bestand met behulp van de export_csv() functie, wat een handige functie is voor het delen van gegevens met anderen.

Schematische weergave van de code:

```mermaid
graph TB;
    
    Begin("Start")
    Begin --> StartBuy
    Begin ---> Date
    Begin --> BasicStart
    Begin --> StartSell

   
    

    subgraph Date functions
        Date -.- GetToday
        SetToday("Set_Today()") -->|"$ python super.py \nset_today yyyy-mm-dd"| Date
    end

    subgraph Core Functionality
        direction TB
       
        BasicStart ==> GetInventory

        GetInventory("GetInventory()")
        
        Inventory -.-> GetInventory

        GetInventory ==> Expired

        GetToday("Get_Today()") <-.- Expired

        Expired --->|yes| ExpiredProducts
        Expired -->|no| Inventory
        
        Expired{"expired?"}
        Inventory[("Inventory")]
        ExpiredProducts[("Expired Products")]
        BasicStart(EveryTime)
    end

    subgraph Sell Function
        StartSell("Sell")

        StartSell -->|"$python super.py \n"| B

        B("sell_products()")
        B --> Inventory

        Inventory --> OnStock

        OnStock{"on stock?"}
        OnStock -->|no| End
        OnStock -->|yes| Sold
        Sold[("Sold Products")]
    end
    subgraph Buy Function
        StartBuy --> BuyProducts
        BuyProducts -->|"$python super.py \nbuy \n--product-name 'Product Name' \n--price buy_price \n--expiration-date YYYY-MM-DD \n--quantity 5"| A

        A --> LinePerProduct
        A --> LinePerPrice
        A --> LinePerExpDate
        
        LinePerProduct --> Products
        LinePerPrice --> Products
        LinePerExpDate --> Products

        Products ==> BoughtProducts
        A("buy_products ()")
        BuyProducts("Buy")

        BoughtProducts[("Bought Products")]

        BoughtProducts --> Expired

    end

    subgraph Report Functions
        direction BT
        Reports(Reports)
        InventoryReport(Inventory\nReport)
        RevenueReport(Revenue\nReport)
        ProfitReport(Profit\nReport)

        Reports --- InventoryReport
        Reports --- ExpiredReport
        Reports --- RevenueReport
        Reports --- ProfitReport

        Date -.- InventoryReport
        Date -.- CalculateProfit
        Date -.- CalculateRevenue

        Inventory <-.- InventoryReport

        InventoryReport --> Inventory_CLIReport
        InventoryReport --> Inventory_CSVReport

        Inventory_CLIReport>CLI Report]
        Inventory_CSVReport>CSV Report]

        ExpiredProducts <-.- ExpiredReport

        ExpiredReport --> Expired_CLIReport
        ExpiredReport --> Expired_CSVReport

        Expired_CLIReport>CLI Report]
        Expired_CSVReport>CSV Report]

        Sold -.-> CalculateProfit

        CalculateProfit --> ProfitReport

        CalculateProfit("Calculate profit")

        ProfitReport --> Profit_CLIReport
        ProfitReport --> Profit_CSVReport

        Profit_CLIReport>CLI Report]
        Profit_CSVReport>CSV Report]

        Sold -.-> CalculateRevenue
        BoughtProducts -.-> CalculateRevenue

        CalculateRevenue -.-> RevenueReport

        RevenueReport --> Revenue_CLIReport
        RevenueReport --> Revenue_CSVReport

        Revenue_CLIReport>CLI Report]
        Revenue_CSVReport>CSV Report]


      
    end
```




