import AVFoundation
import AppKit
let args = CommandLine.arguments
let asset = AVURLAsset(url: URL(fileURLWithPath: args[1]))
let gen = AVAssetImageGenerator(asset: asset)
gen.requestedTimeToleranceBefore = .zero; gen.requestedTimeToleranceAfter = .zero
gen.appliesPreferredTrackTransform = true
let dur = CMTimeGetSeconds(asset.duration)
print("duration", dur, asset.tracks(withMediaType: .video).first?.naturalSize ?? .zero, asset.tracks(withMediaType: .video).first?.nominalFrameRate ?? 0)
for a in args.dropFirst(3) {
  guard let t = Double(a) else { continue }
  if let cg = try? gen.copyCGImage(at: CMTime(seconds: t, preferredTimescale: 600), actualTime: nil) {
    let rep = NSBitmapImageRep(cgImage: cg)
    try? rep.representation(using: .png, properties: [:])?.write(to: URL(fileURLWithPath: "\(args[2])/f\(String(format: "%06.2f", t)).png"))
  }
}
