import PDFKit
import AppKit
// Renders PDF pages to PNG with macOS PDFKit, for scanned SSB publications
// (JBIG2) that pypdf cannot decode.
// Build: swiftc -O scripts/tools/render_pdf_pages.swift -o render_pdf_pages
// Usage: render_pdf_pages <pdf> <outdir> <first page> <last page> [scale]
let a = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: a[1]))!
let scale = a.count > 5 ? CGFloat(Double(a[5])!) : 1.5
for i in Int(a[3])!...Int(a[4])! {
    guard let page = doc.page(at: i - 1) else { continue }
    let box = page.bounds(for: .mediaBox)
    let size = NSSize(width: box.width * scale, height: box.height * scale)
    let img = page.thumbnail(of: size, for: .mediaBox)
    let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
    let png = rep.representation(using: .png, properties: [:])!
    try! png.write(to: URL(fileURLWithPath: "\(a[2])/p\(i).png"))
}
print("done")
