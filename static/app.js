/*
================================================================>
|   Author      |   Ryan Woodward
|   Date        |   May 2024
|   Project     |   Aegis (Inventory System)
================================================================>
*/

/*
    This function allows the user to hide and show the three windows
    based on the icons in the navbar. DB, Inventory Transaction, and 
    overdue returns.
*/
function toggleWindow(windowId) 
{
    const windowElement = document.getElementById(windowId);
    
    if (windowElement) 
    {
        const isVisible = windowElement.style.display !== 'none';
        windowElement.style.display = isVisible ? 'none' : 'block';
        console.log(windowId + ' visibility:', !isVisible);
    } 
    else 
    {
        console.error('Element with ID ' + windowId + ' not found.');
    }
}


function showForm(selectedFormId) 
{

    const returnItemForm    = document.getElementById('return-item-form');
    const checkoutItemForm  = document.getElementById('checkout-item-form');
    const createItemForm    = document.getElementById('create-item-form');
    const updateItemForm    = document.getElementById('update-item-form');
    const deleteItemForm    = document.getElementById('delete-item-form');

    const inventoryTransactions = [];
    inventoryTransactions[0] = returnItemForm;
    inventoryTransactions[1] = checkoutItemForm;
    inventoryTransactions[2] = createItemForm;
    inventoryTransactions[3] = updateItemForm;
    inventoryTransactions[4] = deleteItemForm;

    for (let i = 0; i < inventoryTransactions.length; i++) 
    {

        if (inventoryTransactions[i].id === selectedFormId) 
        {
            inventoryTransactions[i].style.display = 'block';
        } 
        else 
        {
            inventoryTransactions[i].style.display = 'none';
        }
    }
}


window.onload = function() {
    showForm('return-item-form');
};