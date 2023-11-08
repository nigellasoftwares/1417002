using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Printing;

namespace PrintService
{
    class Program
    {
        static void Main(string[] args)
        {
                if (args.Length < 2)
        {
            Console.WriteLine("Usage: Program.exe [imagePath] [textToPrint]");
            return;
        }

        string imagePath = args[0];
        string text = args[1];

            // Automatically detect the default printer
            string printerName = GetDefaultPrinter();

            if (printerName == null)
            {
                Console.WriteLine("No printers found.");
                return;
            }

            Console.WriteLine("Using printer: " + printerName);

            try
            {
                // Create a PrintDocument instance
                PrintDocument pd = new PrintDocument();

                // Use the detected printer as the target printer
                pd.PrinterSettings.PrinterName = printerName;

                // Subscribe to the PrintPage event
                pd.PrintPage += (sender, e) =>
                {
                    // Calculate the image size for 3x3 cm based on printer DPI
                    float desiredWidth = 1.0f * e.Graphics.DpiX / 6.54f; // Set width to 2.8 cm
                    float desiredHeight = 1.0f * e.Graphics.DpiY / 6.54f; // Convert cm to inches

                    // Calculate the position to center the image and text
                    float x = (e.PageBounds.Width - desiredWidth) / 2;
                    float y = (e.PageBounds.Height - desiredHeight) / 2;

                    // Create a rectangle that surrounds both the image and text
                    RectangleF borderArea = new RectangleF(x, y, desiredWidth, desiredHeight + 20); // Added 20 for text

                    // Create a GraphicsPath for the border
                    GraphicsPath borderPath = new GraphicsPath();
                    borderPath.AddRectangle(borderArea);
                    borderPath.Widen(new Pen(Color.Black, 1.0f)); // Create a widened border

                    // Set the clip region to create the border outside the image and text
                    e.Graphics.SetClip(borderPath, CombineMode.Exclude);

                    // Draw the border
                    e.Graphics.DrawPath(new Pen(Color.Black, 1.0f), borderPath);

                    Image img = Image.FromFile(imagePath);

                    // Draw the image centered on the page
                    e.Graphics.DrawImage(img, x, y, desiredWidth, desiredHeight);

                  
                    Font textFont = new Font("Arial", 08, FontStyle.Bold); // Make the font bold

                    // Calculate the text area rectangle
                    float textY = y + desiredHeight - 5; // Adjust vertical position
                    RectangleF textArea = new RectangleF(x, textY, desiredWidth, 30);

                    // Calculate the maximum font size that fits the text within the text area
                    float maxFontSize = 10; // Set a maximum font size
                    SizeF textSize;
                    using (Font testFont = new Font(textFont.FontFamily, maxFontSize))
                    {
                        textSize = e.Graphics.MeasureString(text, testFont);
                        while (textSize.Width > textArea.Width)
                        {
                            maxFontSize -= 0.1f; // Decrease font size until it fits
                            testFont.Dispose();
                            using (Font newFont = new Font(textFont.FontFamily, maxFontSize))
                            {
                                textSize = e.Graphics.MeasureString(text, newFont);
                            }
                        }
                    }

                    // Draw the text with the calculated font size
                    using (Font finalFont = new Font(textFont.FontFamily, maxFontSize))
                    {
                        e.Graphics.DrawString(text, finalFont, Brushes.Black, textArea);
                    }
                };

                // Start the print job
                pd.Print();
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error: " + ex.Message);
            }
        }

        // Function to detect the default printer
        static string GetDefaultPrinter()
        {
            string printerName = null;

            foreach (string printer in PrinterSettings.InstalledPrinters)
            {
                printerName = printer;
                break;
            }

            return printerName;
        }
    }
}
